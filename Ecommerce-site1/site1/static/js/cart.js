
// Add to the cart button

var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtns.length; i++)
    {
    updateBtns[i].addEventListener('click', function()
        {
        // Catching product id and action (which is to add)when the button is clicked
        var productId = this.dataset.product
        var action = this.dataset.action
        // here 'this' is like (self) in python. this represents the button itself which is clicked
        console.log('ProductId:', productId, 'Action:', action)

        // Catching user's name

        console.log('User:', user)
        //Now let's check if the user is logged in or not
        // logged in user's name if a user is logged in.
        // 'Anonymous' if user is not logged in (Guest User)
        if (user == 'AnonymousUser')
            {
            //Cookie for guest - 2.5
            //Replacing the console.log with the function

            //console.log('User is not logged in.')
            addCookieItem(productId, action)
            //Cookie for guest - 2.5 - close
            }
        else
            {
            //console.log('User is logged in, sending data...')

            updateUserOrder(productId, action)
            }
    })
}

//Cookie for guest - 2
function addCookieItem(productId, action) {
    //Writing the console.log here and removing from the if condition used above
    console.log('User is not logged in even from the function - addCookieItem().')

    //>1. Adding the item for the first time
    //>2. If the item already exists then either increasing or decreasing quantity
    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity': 1}
        }
        else {
            cart[productId]['quantity'] += 1
        }
    }
    if (action == 'remove') {
        cart[productId]['quantity'] -= 1

        if (cart[productId]['quantity'] <= 0) {
            console.log('Item should be deleted.')
            delete cart[productId]
        }
    }
    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"

    location.reload()
}
//Cookie for guest - 2 - close

function updateUserOrder(productId, action)
    {
    console.log('User is logged in, sending data...')

    var url = '/update-item/'
    // This url '/update-item/' comes from the urls.py in the app-folder,
    //from this line of code: path('update-item/', views.updateItem, name='store-update-item')

    //Using the fetch API to make a POST request,
    //which is generally done by using <form> tag.
    //So, in order to create a csrf token, a piece of code (from - https://docs.djangoproject.com/en/3.1/ref/csrf/) is written
    //in <script> tag within main.html or base.html
    //If we do not write special piece of code within main.html or base.html
    //we get these two errors:
    //cart.js:51 POST http://127.0.0.1:8000/update-item/ 403 (Forbidden)
    //Uncaught (in promise) SyntaxError: Unexpected token < in JSON at position 1

    //>>Setting the url by the fetch API
    fetch(url,
        {
        //>>type of request is POST
        method: 'POST',
        //>>Passing the data
        headers:
            {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            },
        body:JSON.stringify({'productId': productId, 'action': action})
        })
    //>>Receiving the response in json format
    .then((response) =>
        {
        return response.json()
        })
    //Turning the response into console output
    .then((data) =>
        {
        console.log('Data:', data)
        //Showing the total count of the selected items on the cart icon
        //This has to be done by using REST API. However, we doing it by
        //refreshing the page. So, every click on 'Add to cart' button
        //will add item and shows the count by refreshing the page.
        //Later, I want to replace this whole process with REST API.
        //Cart count-1
        location.reload()
        });
}

