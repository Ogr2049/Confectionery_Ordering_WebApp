
const plusCart = (cart_product_id, quantity) => (
        $.ajax({
            type: "GET",
            url: "/plus_cart/",
            data: {
                'cart_product_id': cart_product_id, "quantity": quantity
            },
            success: (res) => {
				cartList.innerHTML = ``;
				var items = ``;
				for (let cart_product of res.cart_products) {

					items += `
						<div  class="cart-item br-10">
							<div style="    display: flex;
    align-items: center;
    width: 100%;">
							<a href="/catalog/${cart_product.slug}/" class="img">
								<img style="    height: inherit; object-fit: contain;" src="${cart_product.image}" alt="product">
							</a>
                                                        <div class="cart-desc">
							<a href="/catalog/${cart_product.slug}/" class="title">${cart_product.title}</a>
                                                              <p class="product-price">${cart_product.price} ₽ за штуку</p>
                                                        </div>
								</div>
								<div style="    display: flex
;
    align-items: center;
    width: 40%;">
                                                        <div class="quantity-count br-10">
								<a data-id="${cart_product.id}" href="javascript:void(0)" class="dec"></a>
								<input data-id="${cart_product.id}" class="number-text" type="number" value="${cart_product.quantity}">
                                                          	<a data-id="${cart_product.id}" href="javascript:void(0)" class="inc"></a>
							</div>
							<p class="price">${cart_product.total_price} ₽</p>
                            <a data-id="${cart_product.id}" href="javascript:void(0)" class="delete-product">
                                   <img src="/static/img/delete.png" style="width: 24px;">
                            </a>
									</div>
						</div>
					`;
				}
				cartList.innerHTML = items;
				var plusButtons = document.querySelectorAll(".inc");
				var minusButtons = document.querySelectorAll(".dec");
				for (let button of plusButtons) {
					button.onclick = function () {
						plusCart(button.getAttribute("data-id"), false);
					}
				}
				for (let button of minusButtons) {
					button.onclick = function () {
					      if (Number(document.querySelector(`.number-text[data-id="${button.getAttribute('data-id')}"]`).value) !== 1) {
                            minusCart(button.getAttribute("data-id"));
                        }

                                        }
				}


                                var numberInputs = document.querySelectorAll(".number-text");

        for (let input of numberInputs) {
             input.onchange = function () {
                 plusCart(input.getAttribute("data-id"), input.value);
             }
        }
var deleteButtons = document.querySelectorAll(".delete-product");

        for (let button of deleteButtons) {
           button.onclick = function () {
               deleteCart(button.getAttribute("data-id"));
           }
        }


				quantityAll.textContent = res.quantity_all;
                                quantityHeader.textContent = `[${res.quantity_all}]`;
				totalPrice.textContent = `${res.total_price} ₽`;
            },
            error: (err) => {
                console.log(err);
            }
        })
    );

    const minusCart = (cart_product_id) => (
        $.ajax({
            type: "GET",
            url: "/minus_cart/",
            data: {
                'cart_product_id': cart_product_id
            },
            success: (res) => {
				cartList.innerHTML = ``;
				var items = ``;
				for (let cart_product of res.cart_products) {

                                        items += `
                                                <div  class="cart-item br-10">
							<div style="    display: flex;
    align-items: center;
    width: 100%;">
							<a href="/catalog/${cart_product.slug}/" class="img">
								<img style="    height: inherit; object-fit: contain;" src="${cart_product.image}" alt="product">
							</a>
                                                        <div class="cart-desc">
							<a href="/catalog/${cart_product.slug}/" class="title">${cart_product.title}</a>
                                                              <p class="product-price">${cart_product.price} ₽ за штуку</p>
                                                        </div>
								</div>
								<div style="    display: flex
;
    align-items: center;
    width: 40%;">
                                                        <div class="quantity-count br-10">
								<a data-id="${cart_product.id}" href="javascript:void(0)" class="dec"></a>
								<input data-id="${cart_product.id}" class="number-text" type="number" value="${cart_product.quantity}">
                                                          	<a data-id="${cart_product.id}" href="javascript:void(0)" class="inc"></a>
							</div>
							<p class="price">${cart_product.total_price} ₽</p>
                            <a data-id="${cart_product.id}" href="javascript:void(0)" class="delete-product">
                                   <img src="/static/img/delete.png" style="width: 24px;">
                            </a>
									</div>
						</div>
                                        `;

                                }
				cartList.innerHTML = items;
				var plusButtons = document.querySelectorAll(".inc");
				var minusButtons = document.querySelectorAll(".dec");
				for (let button of plusButtons) {
					button.onclick = function () {
						plusCart(button.getAttribute("data-id"), false);
					}
				}


				for (let button of minusButtons) {
					button.onclick = function () {
					       if (Number(document.querySelector(`.number-text[data-id="${button.getAttribute('data-id')}"]`).value) !== 1) {
                            minusCart(button.getAttribute("data-id"));
                        }

                                          }
				}

                               var numberInputs = document.querySelectorAll(".number-text");

        for (let input of numberInputs) {
             input.onchange = function () {
                 plusCart(input.getAttribute("data-id"), input.value);
             }
        }

 var deleteButtons = document.querySelectorAll(".delete-product");

        for (let button of deleteButtons) {
           button.onclick = function () {
               deleteCart(button.getAttribute("data-id"));
           }
        }

				quantityHeader.textContent = `[${res.quantity_all}]`;
                                quantityAll.textContent = res.quantity_all;
				totalPrice.textContent = `${res.total_price} ₽`;
            },
            error: (err) => {
                console.log(err);
            }
        })
    );

        const deleteCart = (cart_product_id) => (
        $.ajax({
            type: "GET",
            url: "/delete_product/",
            data: {
                'cart_product_id': cart_product_id
            },
            success: (res) => {
                                if (Number(res.quantity_all) === 0) {
                                    location.reload()
                                }
                                cartList.innerHTML = ``;
                                var items = ``;
                                for (let cart_product of res.cart_products) {

                                        items += `
                                                <div  class="cart-item br-10">
							<div style="    display: flex;
    align-items: center;
    width: 100%;">
							<a href="/catalog/${cart_product.slug}/" class="img">
								<img style="    height: inherit; object-fit: contain;" src="${cart_product.image}" alt="product">
							</a>
                                                        <div class="cart-desc">
							<a href="/catalog/${cart_product.slug}/" class="title">${cart_product.title}</a>
                                                              <p class="product-price">${cart_product.price} ₽ за штуку</p>
                                                        </div>
								</div>
								<div style="    display: flex
;
    align-items: center;
    width: 40%;">
                                                        <div class="quantity-count br-10">
								<a data-id="${cart_product.id}" href="javascript:void(0)" class="dec"></a>
								<input data-id="${cart_product.id}" class="number-text" type="number" value="${cart_product.quantity}">
                                                          	<a data-id="${cart_product.id}" href="javascript:void(0)" class="inc"></a>
							</div>
							<p class="price">${cart_product.total_price} ₽</p>
                            <a data-id="${cart_product.id}" href="javascript:void(0)" class="delete-product">
                                   <img src="/static/img/delete.png" style="width: 24px;">
                            </a>
									</div>
						</div>
                                        `;
                                }
                                cartList.innerHTML = items;
                                var plusButtons = document.querySelectorAll(".inc");
                                var minusButtons = document.querySelectorAll(".dec");
                                for (let button of plusButtons) {
                                        button.onclick = function () {
                                                plusCart(button.getAttribute("data-id"), false);
                                        }
                                }


                                for (let button of minusButtons) {
                                        button.onclick = function () {
                                            if (Number(document.querySelector(`.number-text[data-id="${button.getAttribute('data-id')}"]`).value) !== 1) {
                                               minusCart(button.getAttribute("data-id"));
                                            }

                                        }
                                }

                               var numberInputs = document.querySelectorAll(".number-text");

        for (let input of numberInputs) {
             input.onchange = function () {
                 plusCart(input.getAttribute("data-id"), input.value);
             }
        }
                                var deleteButtons = document.querySelectorAll(".delete-product");

        for (let button of deleteButtons) {
           button.onclick = function () {
               deleteCart(button.getAttribute("data-id"));
           }
        }


                                quantityAll.textContent = res.quantity_all;
                                quantityHeader.textContent = `[${res.quantity_all}]`;
                                totalPrice.textContent = `${res.total_price} ₽`;
            },
            error: (err) => {
                console.log(err);
            }
        })
    );

        var quantityHeader = document.querySelector("#cart-count");
	var cartList = document.querySelector(".cart-items-list");
	var quantityAll = document.querySelector("#quantity-all");
	var totalPrice = document.querySelector("#total-price");
	var plusButtons = document.querySelectorAll(".inc");
	var minusButtons = document.querySelectorAll(".dec");
        var deleteButtons = document.querySelectorAll(".delete-product");

        for (let button of deleteButtons) {
           button.onclick = function () {
               deleteCart(button.getAttribute("data-id"));
           }
        }



	for (let button of plusButtons) {
		button.onclick = function () {
			plusCart(button.getAttribute("data-id"), false);
		}
	}

	for (let button of minusButtons) {
		button.onclick = function () {
                        if (Number(document.querySelector(`.number-text[data-id="${button.getAttribute('data-id')}"]`).value) !== 1) {
			    minusCart(button.getAttribute("data-id"));
		        }
                }
	}


        var numberInputs = document.querySelectorAll(".number-text");

        for (let input of numberInputs) {
             input.onchange = function () {
                 plusCart(input.getAttribute("data-id"), input.value);
             }
        }

