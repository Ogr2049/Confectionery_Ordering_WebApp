var selectors = document.querySelectorAll(".selector-button");

for (let selector of selectors) {
    selector.onclick = function () {
      selector.classList.toggle("active");
    };
};

var selectorsValues = document.querySelector("#order-catalog");

if (selectorsValues) {
for (let label of selectorsValues.querySelectorAll("label")) {
    label.onclick = function () {
        document.querySelector("#order-catalog").querySelector(".selector-button").classList.remove('active');
        document.querySelector("#order-catalog").querySelector(".selector-button").querySelector(".name").textContent = label.textContent;
    };
}
}

const orderCatalog = (category_slug, sort) => (
            $.ajax({
                type: "GET",
                url: "/order-sort",
                data: {
                    'category_slug': category_slug,
                    'sort': sort
                },
                success: (res) => {
	    			containerProducts.innerHTML = ``;
	    			var products = ``;

	    			for (let product of res.products) {
                          let in_cart = ``;
                          let redirect_cart = "";

                          if (product.in_cart) {
                              in_cart = "in-cart";
                              redirect_cart = `onclick="document.location.href='/cart/'"`;
                          } else {
                              in_cart = "add-to-cart";
                          }

                          products += `<div class="catalog-product-item">
                                <div class="product-item br-15" data-id="${product.id}">
    <div class="product-item-image">
        <img src="${product.image}" alt="${product.title}">
        <a href="/catalog/${product.slug}/" class="link"></a>
    </div>
    <div class="product-item-body">
        <a href="/catalog/${product.slug}/" class="product-title">${product.title} ${product.weight}</a>
        <div class="product-bottom">
                <p class="bottom-price">${product.price} ₽</p>
                         <div ${redirect_cart} data-id="${product.id}"  class="bottom-cart ${in_cart} br-10"></div>

    </div>
</div>
</div></div>`;
	    			}
	    			containerProducts.innerHTML = products;

                },
                error: (err) => {
                    console.log(err);
                }
            })
        );


var orderInputs = document.querySelectorAll(`input[name="order"]`);
var containerProducts = document.querySelector("#catalog-listing");


for (let input of orderInputs) {
    input.onchange = function () {
        let activeCategory = document.querySelector("#active-category").value;
        orderCatalog(activeCategory, input.getAttribute("data-name"));
    };
}

var loginButton = document.querySelector("#submit-login");

if (loginButton) {
  loginButton.onclick = function () {
     var loginForm = document.querySelector("#login-form");
     for (let input of loginForm.querySelectorAll(".required")) {
       if (!input.value) {
          input.style.borderColor = "red";
          return false;
       }
     }
    loginForm.submit();
}
}

const addCartCard = (product_id) => (
        $.ajax({
            type: "GET",
            url: "/add_cart/",
            data: {
                'product_id': product_id
            },
            success: (res) => {
            },
            error: (err) => {
                console.log(err);
            }
        })
);

var countHeader = document.querySelector(".count-header");
var addCartButtons = document.querySelectorAll(".bottom-cart");

for (let button of addCartButtons) {
        let buttons = document.querySelectorAll(`.bottom-cart[data-id="${button.getAttribute('data-id')}"]`);
        for (let button2 of buttons) {
		    button2.onclick = function () {
                 if (!button2.classList.contains("in-cart")) {
			        addCartCard(button2.getAttribute("data-id"));
                    button2.classList.add("in-cart");
                    button2.onclick = function () {
                        document.location.href = "/cart";
                    }
                 }
				countHeader.textContent = Number(countHeader.textContent) + 1;
		    }
        }
}