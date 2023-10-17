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
