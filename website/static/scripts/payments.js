function addCredit(id) {
    credit = document.getElementById("amountToBeAdded").value
    console.log(credit)
    if(credit == "") 
    return
    if (credit < 100) 
    document.getElementById('result').innerHTML = "You can't add less than 100 credits"
    else{
        fetch(`/users/payments/${id}/add/${credit}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json())
            .then(data => {
                setAlert('success',`Successfully added ${credit} credits`)
                    document.getElementById('userCredit').innerHTML = parseInt(document.getElementById('userCredit').innerHTML) + parseInt(credit)
                    document.getElementById('amountToBeAdded').value = ""

                    const t = data.payment
                    var date = new Date(t.date)
                    date = date.toISOString().substring(0, 10);
                    row = ` <tr id="${ t.id }" class="border-blue-900 border-2 border-t-0 mb-2 sm:mb-0 hover:bg-blue-50 mb-2">
                        <td class="border-blue-900 border p-2 text-center">${t.id }</td>
                        <td class="border-blue-900 border p-2 text-center">${ t.amount }</td>
                        <td class="border-blue-900 border p-2 text-center">${ date }</td>
                    </tr>`
                    document.getElementById('usersPaymentTableContent').innerHTML += row
            })
    }
}