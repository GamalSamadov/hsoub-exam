let stripe, elements;
const stripeSubmit = document.getElementById('stripe-submit');

async function createStripeSession() {

  stripeSubmit.disabled = true;
  try {
    const { data } = await axios.post("/checkout/stripe")
    const { client_secret } = data;

    const appearance = { theme: 'flat' };
    elements = stripe.elements({ appearance, clientSecret: client_secret });
    const paymentElement = elements.create("payment")
    paymentElement.mount("#payment-element");

    document
    .querySelector("#payment-form")
    .addEventListener("submit", _stripeFormSubmit);

    document.getElementById('stripe-card').style.display = 'block'
    stripeSubmit.disabled = false;
  } catch (e) {
    console.log(e)
    notyf.error(e.response.data.message);
  }
}

async function _stripeFormSubmit(e) {
  e.preventDefault();
  stripeSubmit.disabled = true;
  const host = window.location.protocol + "//" + window.location.host;
  const { error } = await stripe.confirmPayment({
    elements,
    confirmParams: {
      return_url: `${host}/checkout/complete`,
    },
  });

  if (error.type === "card_error" || error.type === "validation_error") {
    Toastify({
      text: error.message,
      duration: 3000,
      newWindow: true,
      close: true,
      gravity: 'top',
      position: 'right',
      stopOnFocus: true,
      style: {
        background: 'linear-gradient(to right, #b02f00, #96572d)'
      },
      onClick: function () {} // Callback after click
    }).showToast()
  } else {
    Toastify({
      text: "Sorry, an error occurred during the payment process.",
      duration: 3000,
      newWindow: true,
      close: true,
      gravity: 'top',
      position: 'right',
      stopOnFocus: true,
      style: {
        background: 'linear-gradient(to right, #b02f00, #96572d)'
      },
      onClick: function () {} // Callback after click
    }).showToast()
  }
  stripeSubmit.disabled = false;
}

async function _checkStripePaymentStatus() {
  const clientSecret = new URLSearchParams(window.location.search).get(
    "payment_intent_client_secret"
  );
  if (!clientSecret) {
    return;
  }
  const { paymentIntent } = await stripe.retrievePaymentIntent(clientSecret);
  switch (paymentIntent.status) {
    case "succeeded":
      Toastify({
        text: 'The payment was completed successfully',
        duration: 3000,
        newWindow: true,
        close: true,
        gravity: 'top',
        position: 'right',
        stopOnFocus: true,
        style: {
          background: 'linear-gradient(to right, #00b09b, #70962d)'
        },
        onClick: function () {} // Callback after click
      }).showToast()
      break;
    case "processing":
      Toastify({
        text: 'The payment is being processed',
        duration: 3000,
        newWindow: true,
        close: true,
        gravity: 'top',
        position: 'right',
        stopOnFocus: true,
        style: {
          background: 'linear-gradient(to right, #00b09b, #70962d)'
        },
        onClick: function () {} // Callback after click
      }).showToast()
      break;
    default:
      Toastify({
        text: "Sorry, there was an error during the payment process",
        duration: 3000,
        newWindow: true,
        close: true,
        gravity: 'top',
        position: 'right',
        stopOnFocus: true,
        style: {
          background: 'linear-gradient(to right, #b02f00, #96572d)'
        },
        onClick: function () {} // Callback after click
      }).showToast()
      break;
  }
}

async function _stripeInit() {
    const { data } = await axios("/checkout/stripe/config");
    stripe = Stripe(data.public_key, { locale: 'en' });
    _checkStripePaymentStatus();
}

_stripeInit();
