async function cartUpdate(e) {

  const { data } = await axios(e.dataset.url)
  const { message, items_count } = data

  Toastify({
    text: message,
    duration: 3000,
    newWindow: true,
    close: true,
    gravity: 'top',
    position: 'right',
    stopOnFocus: true,
    style: {
      background: 'linear-gradient(to right, #00b09b, #70962d)'
    },
    onClick: function () { } // Callback after click
  }).showToast()

  document.getElementById("cart-items-count").innerHTML = items_count

}


async function cartRemove(e) {
  await axios(e.dataset.url)
  location.reload()
}


async function cartEmpty() {
  await axios('/cart/remove')
  location.reload()
}

function switchPaymentMethod(type, content) {
 const stripeCard = document.getElementById('stripe-card');
 const stripePaymentElement = document.getElementById('payment-element');
 const paypalCard = document.getElementById('paypal-card');
 if (type === 'stripe') {
     paypalCard.style.display = 'none'
     stripeCard.style.display = 'block'
     paypalCard.innerHTML = ''
 } else {
     stripeCard.style.display = 'none'
     paypalCard.style.display = 'block'
     stripePaymentElement.innerHTML = ''
     paypalCard.innerHTML = content
 }
}

async function createPaypalSession() {
 try {
     const form = document.getElementById('form-user-info');
     const formData = new FormData(form);
     const { data } = await axios.post("/checkout/paypal", formData);
     switchPaymentMethod('paypal', data)
 } catch (e) {
     notyf.error(e.response.data.message);
 }
}