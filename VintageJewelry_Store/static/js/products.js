//url = 'http://127.0.0.1:8000/products/'
var posts = []
let productList = ''

func1();

function func1(){
    url = document.URL + 'products/';
    document.getElementById("products").innerHTML = "";

    if(document.getElementById('selectid').value == "price_asc") {
        url += "?ordering=price"
    }
    else if(document.getElementById('selectid').value == "price_desc") {
        url += "?ordering=-price"
    }
    if(document.getElementById("searchfield").value != ''){
        url += "&search=" + document.getElementById("searchfield").value;
    }

    fetch(url, {
    method: "GET",
    headers: {"Content-type": "application/json;charset=UTF-8"}
    })
    .then(res => res.json()).then(res => {
      //if the Key is wrong
      if (res.status == 401) {
          message.channel.send("Your API key is not valable, please set a valable one with !setinfo command followed by your key");
      }
      //if the Key is valid
      else {
          res['results'].forEach(element => {
              productList += 
              `<div class="col">
              <div class="card-product">`
              element["images"].forEach(el => {
                  productList += `<img class="card-img-top" src="${el["image"]}">`
              })
              productList += `<div class="card-body">
                  <h4 class="card-title">${element["name"]}</h4>
                  <p class="card-text">${element["description"]}</p>
                  <button class="btn btn-info" data-toggle="modal"
                  data-target="#productInfoModal" data-id="${element["id"]}">Info
                  </button>
                  <button class="btn btn-primary buy" data-id="${element["id"]}">
                  $${element["price"]} - Buy
                  </button>
                  </div>
                  </div>
                  </div>`;
              var post = {};
              post["id"] = element["id"];
              post["name"] = element["name"];
              post["brand_name"] = element["brand_name"];
              post["material"] = element["material"];
              post["description"] = element["description"];
              post["price"] = element["price"];
              post["amount"] = element["amount"];
              posts.push(post);
          })
          $( "div.main-container" ).html(productList);
        }
      // code to handle the error
    }).catch(err => {});
    posts = [];
    productList = '';
}


$('#productInfoModal').on('show.bs.modal', event => {
    console.log("yes");
    const button = $(event.relatedTarget); // Button that triggered the modal
    const id  = String(button.data('id')); // Extract info from data-* attributes
    var product = posts.find(i =>i["id"]==id);
    const modal = $('#productInfoModal');
    modal.find('.modal-body .card-name').text(product["name"]);
    modal.find('.modal-body .card-brand').text(`Brandname: ${product["brand_name"]}`);
    modal.find('.modal-body .card-material').text(`Material: ${product["material"]}`);
    modal.find('.modal-body .card-description').text(product["description"]);
    modal.find('.modal-body .card-amount').text(`Amount: ${product["amount"]}`);
    modal.find('button.buy')
        .text(`${product["price"]} - Buy`)
        .data('id', id);
});
