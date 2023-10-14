// Get URL object for the current page
var url = new URL(window.location.href);
var coupon = url.searchParams.get("coupon");

if (coupon && coupon.length > 4) {
  // set coupon value
  document.getElementsByName("coupon")[0].value = coupon;

  // show the field
  var couponCollapse = new bootstrap.Collapse(
    document.getElementById("collapse-coupon")
  );
  couponCollapse.show();

  validate();
}

// Function to handle the validateCoupon button without email
function validateCouponWithoutEmail() {
  var form = document.getElementById("payment-form");
  var coupon = document.getElementById("coupon").value;

  if (!coupon) {
    form.reportValidity();
    return false;
  }

  fetch(window.location.origin + "/learn/guest-checkout.php", {
    method: "post",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      action: "validatecoupon",
      coupon: coupon,
    }),
  })
    .then((response) => {
      res = response.json().then((result) => {
        if (result.error) {
          document.getElementById("card-error").style.display = "block";
          document.getElementById("error-msg").innerHTML = "الكوبون غير صالح";
          resetCoupon();
        }
        if (result.amount) {
          document.getElementById("card-error").style.display = "none";
          document.getElementById("validate-coupon").disabled =
            document.getElementById("coupon").disabled = true;
          document.getElementById("pay-button").innerHTML =
            document.getElementById("pay-button").dataset.normalText =
              "اشترك الآن فقط بـ <s style='opacity: 0.5;'>290$</s> " +
              (290 - result.amount) +
              "$";
        }
      });
    })
    .catch((error) => {
      console.error("Error validating:", error);
    });
}

// Function to handle the validateCoupon button with email
function validateCouponWithEmail() {
  var form = document.getElementById("payment-form");
  var email = document.getElementById("email").value;
  var coupon = document.getElementById("coupon").value;

  if (!email || !coupon) {
    form.reportValidity();
    return false;
  }

  fetch(window.location.origin + "/learn/guest-checkout.php", {
    method: "post",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      action: "validatecouponwithemail",
      email: email,
      coupon: coupon,
    }),
  })
    .then((response) => {
      res = response.json().then((result) => {
        if (result.error) {
          document.getElementById("card-error").style.display = "block";
          document.getElementById("error-msg").innerHTML = "الكوبون غير صالح";
          resetCoupon();
        }
        if (result.amount) {
          document.getElementById("card-error").style.display = "none";
          document.getElementById("validate-coupon").disabled =
            document.getElementById("coupon").disabled = true;
          document.getElementById("pay-button").innerHTML =
            document.getElementById("pay-button").dataset.normalText =
              "اشترك الآن فقط بـ <s style='opacity: 0.5;'>290$</s> " +
              (290 - result.amount) +
              "$";
        }
      });
    })
    .catch((error) => {
      console.error("Error validating:", error);
    });
}

function resetCoupon() {
  document.getElementById("pay-button").innerHTML = document.getElementById(
    "pay-button"
  ).dataset.normalText = "اشترك الآن فقط بـ 290$";
  document.getElementById("validate-coupon").disabled = document.getElementById(
    "coupon"
  ).disabled = false;
}

function validate() {
  if (document.getElementById("email").value != "") {
    validateCouponWithEmail();
  } else {
    validateCouponWithoutEmail();
  }

}
// Attaching validate coupon to the button
const validateButton = document.getElementById("validate-coupon");
validateButton.addEventListener("click", validate);

// Disable validation button when coupon is empty
document.getElementById("coupon").addEventListener("input", () => {
  document.getElementById("validate-coupon").disabled =
    document.getElementById("coupon").value.trim() === "";
});

// Reset coupon info when email changes
document.getElementById("email").addEventListener("input", () => {
  resetCoupon();
});

// Edge case when setting user email via IPS and coupon via URL
if (
  document.getElementById("coupon").value != "" &&
  document.getElementById("email").value != ""
) {
  document.getElementById("validate-coupon").disabled = false;
  validateCoupon();
}
