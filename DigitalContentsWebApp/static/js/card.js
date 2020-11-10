function card(stripe_publishable_key, customer_email) {
    document.addEventListener("DOMContentLoaded", function(event){
        //instance of js stripe object that takes publishable API key. Creating stripe client
        var stripe = Stripe(stripe_publishable_key);
        //JS stripe library uses an object called "elements", manipulating DOM objects
        var elements = stripe.elements();

        var style = {
          base: {
            color: '#32325d',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
              color: '#aab7c4'
            }
          },
          invalid: {
            color: '#fa755a',
            iconColor: '#fa755a'
          }
        };

        // JS object card and styling it from above. Create an instance of the card Element.
        var card = elements.create('card', {style: style});
        //associating card with DOM element
        // Add an instance of the card Element into the `card-element` <div> in js.html.
        card.mount("#card-element");//DOM must contain div with card-element id in card.html

        // Handle real-time validation errors from the card Element.
       card.addEventListener('change', function(event) {
          var displayError = document.getElementById('card-errors');
          if (event.error) {
            displayError.textContent = event.error.message;
          } else {
            displayError.textContent = '';
          }
       });

       // Catch submit event and handle form submission. From card object, create payment method object.
       //Need to pass payment method's id to the django. Django will use payment method ID to initiate the payment
       var form = document.getElementById('payment-form');
       //add submit event listener to our payment-form
       form.addEventListener('submit', function(event) {
          event.preventDefault();

          //using stripe js, creating a token from the card object.
          //Token object is used to pass info between client and server side
          stripe.createToken(card).then(function(result) {
            if (result.error) {
              // Inform the user if there was an error.
              var errorElement = document.getElementById('card-errors');
              errorElement.textContent = result.error.message;
            } else {
              // Create Payment Method BEGIN. Payment method object is now created.
              /* Payment method object is created from the card object which contains user input and
              uses customer email to identify this payment method object with the customer */
              stripe.createPaymentMethod({
                type: 'card',
                card: card,
                billing_details: {
                  email: customer_email,
                },//pass payment method id  to django side using the function below
              }).then(function(payment_method_result){
                if (payment_method_result.error) {
                  var errorElement = document.getElementById('card-errors');
                  errorElement.textContent = payment_method_result.error.message;
                } else {
                  //Passing id of payment method by creating hidden input element and attaching it to the existing form
                  var form = document.getElementById('payment-form');
                  var hiddenInput = document.createElement('input');

                  hiddenInput.setAttribute('type', 'hidden');
                  hiddenInput.setAttribute('name', 'payment_method_id');
                  hiddenInput.setAttribute('value', payment_method_result.paymentMethod.id);

                  form.appendChild(hiddenInput);
                  // Submits the form using payment method id to the django side
                  form.submit();
                };
              });
              // Create Payment Method END
            }
          }); // createToken

       }); // form.addEventListener(..)

    }); // DOMContentLoaded
}