var page_number = 1

function BtnDisable(value) {
    document.getElementById("bookBtnTwo").disabled = value
}

function viewBook(id) {
    window.location.href = "/books/" + id
}

function getBooks(change) {
    BtnDisable(true)
    if (change + page_number > 0) {
        document.getElementById("booksContent").innerHTML = ''
        document.getElementById("loader").style.display = "inline"
        page_number += change
        document.getElementById("pageNumber").innerHTML = page_number
        fetch("/api/books?page=" + page_number + "&search=" + document.getElementById("search").value + "&author=" + document.getElementById("author").value,
            {
                "method": "GET",
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(function (response) {
                if (response.ok)
                    return response.json();
                else
                    throw response.json();

            }).then(function (data) {
                data = data.items;

                if (data.length > 0) {
                    document.getElementById("loader").style.display = "none"
                    for (var i = 0; i < data.length; i++) {

                        book = data[i]

                        if (!book.volumeInfo.imageLinks) {
                            book.volumeInfo.imageLinks = { "thumbnail": "https://via.placeholder.com/150" }
                        }

                        document.getElementById("booksContent").innerHTML += `<article id="` + book.id + `" class="w-full justify-evenly flex flex-col shadow-lg resources-responsive m-1.5 border-2 hover:bg-blue-50 border-blue-900 p-2 rounded-md transition-linear duration-300">

                    <h1 class="text-xl text-blue-800 font-bold"> `+ book.volumeInfo.title + `</h1>
            
                    <hr class="border border-dashed border-blue-900 my-2">
            
                    <img src="`+ book.volumeInfo.imageLinks.thumbnail + `" class="mx-auto h-48" alt="">

                    <h3 class="self-end text-white my-1 mt-3 flex justify-evenly w-full">
                    <button class="py-0.5 px-4 rounded-full bg-blue-700 hover:bg-blue-900" onclick="addToFavs('${book.id}')">Add ❤️</button>
                    <button class="py-0.5 px-4 rounded-full bg-blue-700 hover:bg-blue-900" onclick="viewBook('${book.id}')">View 👀</button>
                    </h3>
                    
                    </article>`

                    }
                    BtnDisable(false)
                }
                else {
                    document.getElementById("loader").style.display = "none"
                    document.getElementById("booksContent").innerHTML += `<h1 class="text-xl text-red-700 mt-2 font-bold"> No books found</h1>`
                    BtnDisable(true)
                    document.getElementById("bookBtnOne").disabled = false
                }
            }).catch(function (error) {

                const p = Promise.resolve(error)
                p.then(function (data) {
                    document.getElementById("booksContent").innerHTML += `<h1 class="text-xl text-red-700 mt-2 font-bold">${data.error}</h1>`
                })

                document.getElementById("loader").style.display = "none"
                BtnDisable(true)
                document.getElementById("bookBtnOne").disabled = false
            });

    }
}

function filter() {
    document.getElementById("filter").classList.toggle("hidden")
}

function search() {
    getBooks(1 - page_number)
    filter()
}

getBooks(0)