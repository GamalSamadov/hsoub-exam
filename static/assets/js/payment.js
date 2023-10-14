// var paymentIntentUrl = window.location.origin + '/api/core/guestpurchase/';
var stripePublishableKey =
  window.location.host == "localhost"
    ? "pk_test_51LEXo7CqoC6g8SnbfW42UyGMHtfak8cZFKSQe6Xe4KnIJIYa9Ix2SVkEery9HNCErFK2cMFzuhplZKIUpgLF7tUi008DD64jqY"
    : "pk_live_8PgFsQhQKYbCfaRCZYuDO43t";

// Payment function
var stripePay = {
  stripe: null,
  card: null,
  scope: "payment-form",
  key: stripePublishableKey,
  purchaseURL: window.location.origin + "/learn/guest-checkout.php",

  /**
   * Init
   */
  setup: function (key) {
    this.stripe = Stripe(key);
    var elements = this.stripe.elements();
    this.card = elements.create("card");
    this.card.mount("#card_elements");
  },
  /**
   * Submit form action
   *
   * @param        {event}    e        Event object
   * @returns    {void}
   */
  submitForm: function (e) {
    var scope = document.getElementById(stripePay.scope);

    if (
      !e.currentTarget.querySelectorAll(
        'input[type="radio"][name="payment_method"]'
      ).length ||
      e.currentTarget
        .querySelector(
          'input[name="payment_method"][value="' +
            scope.getAttribute("data-id") +
            '"]'
        )
        .getAttribute("checked")
    ) {
      /* Already submitted */
      if (
        e.currentTarget.querySelectorAll(
          'input[name="' + scope.getAttribute("data-id") + '_card[token]"]'
        ).length
      ) {
        return;
      }

      /* Stop the form from actually submitting */
      e.preventDefault();
      e.stopPropagation();

      /* Hide any previous errors */
      setError(false);

      var data = { billing_details: { address: {} } };
      data.billing_details.email = document.getElementById("email").value;
      data.billing_details.name = document.getElementById("card_name").value;
      if (
        scope.getAttribute("data-amount") &&
        parseFloat(scope.getAttribute("data-amount")) > 0
      ) {
        this.stripe
          .createPaymentMethod("card", this.card, data)
          .then(this.receivedCardPaymentMethod);
      } else {
        this.stripe
          .confirmCardSetup(scope.getAttribute("data-setupSecret"), {
            payment_method: {
              card: this.card,
              data,
            },
          })
          .then(function (result) {
            if (result.error) {
              console.log(result);
              setError(result.error);
            } else {
              var input = document.createElement("input");
              input.type = "hidden";
              input.className = "css-class-name"; // set the CSS class
              input.setAttribute(
                "name",
                scope.getAttribute("data-id") + "_card[token]"
              ); // set the CSS class
              input.value = result.setupIntent.payment_method; // set the CSS class

              scope.closest("form").append(input);
              scope.submit();
            }
          });
      }
    }
  },
  /**
   * Create payment intent
   *
   * @param        {mixed}    paymentMethodId        A Stripe payment method ID or a stored card ID
   * @returns    {void}
   */
  createPaymentIntentAndPurchase: function (paymentMethodId) {
    var scope = document.getElementById(this.scope);
    var stripe = this.stripe;
    fetch(this.purchaseURL, {
      method: "post",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        action: "intentAndCharge",
        email: document.querySelector('input[name="email"]').value,
        coupon: document.querySelector('input[name="coupon"]').value,
        paymentMethodId: paymentMethodId,
        courseID: scope.querySelector('input[name="course_id"]').value,
        savePaymentMethod: false,
      }),
    })
      .then((response) => {
        res = response.json().then((value) => {
          if (value.status === "requires_action") {
            stripe
              .handleCardAction(value.client_secret)
              .then(function (result) {
                if (result.error) {
                  var error =
                    stripePay.getError(result.error.code) ||
                    result.error.message;
                  setError(error);
                } else {
                  stripePay.purchaseNow(
                    value.id,
                    document.querySelector('input[name="email"]').value,
                    document.querySelector('input[name="course_id"]').value,
                    value.payment_method
                  );
                }
              });
          } else {
            displayPurchaseResult(value);
          }
        });
      })
      .catch((error) => {
        setError(error);
      });
  },
  /**
   * Callback after a Stripe Payment Method has been generated for a card
   *
   * @param        {object}    result    The result
   * @returns    {void}
   */
  receivedCardPaymentMethod: function (result) {
    /* Init */
    var scope = this.scope;
    /* If there was an error, show the form again */
    if (result.error) {
      console.log("receivedCardPaymentMethod Error ", result.error);
      var error = stripePay.getError(result.error.code) || result.error.message;
      setError(error);
    } else {
      /* Otherwise, process... */
      stripePay.createPaymentIntentAndPurchase(result.paymentMethod.id);
    }
  },
  getError: function (code) {
    var errorMessages = {
      incomplete_number: "رقم البطاقة غير صحيح.",
      incorrect_number: "رقم البطاقة غير صحيح.",
      invalid_number: "رقم بطاقة الائتمان غير صالح.",
      invalid_expiry_month: "شهر انتهاء صلاحية البطاقة غير صالح.",
      invalid_expiry_month_past: "شهر انتهاء صلاحية البطاقة غير صالح.",
      invalid_expiry_year: "سنة انتهاء صلاحية البطاقة غير صالحة.",
      invalid_expiry_year_past: "سنة انتهاء صلاحية البطاقة غير صالحة.",
      invalid_cvc: "رمز أمان البطاقة غير صالح.",
      expired_card: "انتهت صلاحية البطاقة.",
      incorrect_cvc: "رمز أمان البطاقة غير صحيح.",
      incomplete_cvc: "رمز أمان البطاقة غير صحيح.",
      incomplete_zip: "فشل التحقق من صحة الرمز البريدي للبطاقة.",
      incorrect_zip: "فشل التحقق من صحة الرمز البريدي للبطاقة.",
      card_declined: "رفضت البطاقة.",
      missing: "There is no card on a customer that is being charged.",
      processing_error: "حدث خطأ أثناء معالجة البطاقة.",
      email_invalid: "عنوان البريد الإلكتروني غير صالح.",
      rate_limit:
        "حدث خطأ بسبب الطلبات الكثيرة! يرجى إعلامنا إذا كنت تكرر هذا الخطأ معك.",
      payment_intent_authentication_failure: "رفضت المعاملة المالية من طرفك.",
      invalid_account:
        "تواصل مع البنك الذي أصدر البطاقة للتحقق من عملها بشكل صحيح.",
      lost_card: "تواصل مع البنك الذي أصدر البطاقة للتحقق من عملها بشكل صحيح.",
      not_permitted: "لم يتم السماح بالدفع من طرف البنك",
      invalid_amount: "تأكد من رصيد البطاقة.",
      stolen_card: "رفضت البطاقة.",
      do_not_honor: "رفضت البطاقة.",
      generic_decline: "رفضت البطاقة.",
      call_issuer: "تواصل مع البنك لمزيد من المعلومات.",
      currency_not_supported: "البطاقة لا تدعم الدفع بالدولار.",
      insufficient_funds: "لا تحتوي البطاقة على أموال كافية.",
      online_or_offline_pin_required:
        "عملية الدفع تتطلب إدخال رقم التعريف الشخصي.",
      incorrect_pin: "رقم التعريف الشخصي المدخل غير صحيح.",
      incomplete_expiry: "تاريخ انتهاء البطاقة فارغ أو غير مكتمل.",
    };

    return errorMessages[code];
  },
  purchaseNow: function (token, email, course, card) {
    var xtoken = document.querySelector(
      'form[name="stripe"] input[name="token"]'
    ).value;
    var xid = document.querySelector(
      'form[name="stripe"] input[name="id"]'
    ).value;
    var coupon = document.querySelector(
      'form[name="stripe"] input[name="coupon"]'
    ).value;
    var action = "purchase_3ds";

    fetch(this.purchaseURL, {
      method: "post",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        action,
        token: token,
        email: email,
        courseID: course,
        xtoken,
        xid,
        card,
        coupon,
      }),
    })
      .then((response) => {
        res = response.json().then((result) => {
          displayPurchaseResult(result);
        });
      })
      .catch((error) => {
        setError(error);
      });
  },
};
var displayPurchaseResult = function (result) {
  var res = !isJsonString(result) ? result : JSON.parse(result);
  if (res.success) {
    document.getElementById("payment-panel").style.display = "none";
    document.getElementById("pay-alternative").style.display = "none";
    document.getElementById("card-success").style.display = "block";
    sendGASale();
  } else {
    clearLoading();
    document.getElementById("card-error").style.display = "block";
    document.getElementById("error-msg").innerHTML =
      stripePay.getError(res.code) || res.error;
  }
};

var setError = function (error) {
  if (!error) {
    document.getElementById("card-error").style.display = "none";
    return;
  }
  document.getElementById("card-error").style.display = "block";
  document.getElementById("error-msg").innerHTML = error;
  clearLoading();
};

// loading spinner
var setLoading = function () {
  var button = document.getElementById("pay-button");
  if (!button.dataset.normalText) {
    button.dataset.normalText = button.innerHTML;
  }
  button.setAttribute("disabled", "disabled");
  button.innerHTML = button.dataset.loadingText;
};
var clearLoading = function () {
  var button = document.getElementById("pay-button");
  button.removeAttribute("disabled");
  button.innerHTML = button.dataset.normalText;
};

var isJsonString = function (str) {
  try {
    JSON.parse(str);
  } catch (e) {
    return false;
  }
  return true;
};

// on payment form submit
document
  .querySelector('form[name="stripe"]')
  .addEventListener("submit", function (event) {
    setLoading();
    stripePay.submitForm(event);
  });


// send GA sale 
function sendGASale() {
  var courseID = document.querySelector('input[name="course_id"]').value;
  var courses = {
    7: "computer-science",
    1: "front-end-web-development",
    5: "javascript-application-development",
    2: "php-web-application-development",
    10: "product-development-management",
    9: "python-application-development",
    4: "ruby-web-application-development",
  };

  var coupon = document.querySelector('input[name="coupon"]').value;
  var checkout_value = 290; // current price in USD
  if(coupon.length > 1) {
    checkout_value = 190; // coupon -100$
  }

  try {
    gtag('event', 'checkout', {
      'event_category' : 'Store',
      'event_label' : courses[courseID],
      'value': checkout_value
    });

    gtag("event", "purchase", {
      transaction_id: Date.now(),
      value: checkout_value,
      currency: "USD",
      coupon: coupon,
      items: [
        {
          item_id: courseID,
          item_name: courses[courseID],
          discount: checkout_value == 290 ? "0": "100",
          price: 290
        }
      ]
  });
  
  } catch(e) {
    console.error(e);
  }
}
