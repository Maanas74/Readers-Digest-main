function addToFavs(thisbook) {
    // const book = getBookID(thisbook)
    fetch('/api/books/fav/add/' + thisbook, {
        method: 'POST'
    }).then(function (response) {
        if (response.ok)
            return response.json();
        else
            throw response.json();

    }).then(function (data) {
        setAlert("success", data.msg)
    }).catch(function (error) {
        const data = Promise.resolve(error)
        data.then(function (data) {
            setAlert("error", data.error)
        })
    });
}

function removeFromFavs(id) {
    fetch('/api/books/fav/remove/' + id, {
        method: 'DELETE'
    }).then(function (response) {
        if (response.ok)
            return response.json();
        else
            throw response.json();

    }).then(function (data) {
        setAlert("success", data.msg)
    }).catch(function (error) {
        const data = Promise.resolve(error)
        data.then(function (data) {
            setAlert("error", data.error)
        })
    });
    var table = document.getElementById("favBooks");
    var rowIndex = document.getElementById(id).rowIndex;
    table.deleteRow(rowIndex);
}



