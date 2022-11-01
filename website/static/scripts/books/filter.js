// function to filter transactions by status all returned and acitve
function filterTransactions(status) 
{

if (status == "True")
status = true  
else if (status == "False")
status = false 

const table = document.getElementById('booksTableContent')
var rows = table.getElementsByTagName('tr')

for (var i = 0; i < rows.length; i++)
{
    value = rows[i].getElementsByTagName('td')[4].textContent
    rows[i].style.display = 'table-row'

    if(status == "All")
    value = status
    else if (value == "Active")
    value = true  
    else
    value = false 

    console.log(value, status)

    if (value != status)
    rows[i].style.display = 'none'
}

}




