function issueBook(book)
    {
        member = document.getElementById("member").value
        fetch(`/users/${member}/issue/${book}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            }
          }).then(function (response) {
            if (response.ok)
            return response.json();
            else
            throw response.json();
          }).then(function (data) {

                 console.log(data)
                 data = data.issued
                  const t = data
                  var date = new Date(t.issued)
                  date = date.toISOString().substring(0, 10);
                  document.getElementById('usersTableContent').innerHTML += ` <tr id="${t.id}" class="border-blue-900 border-2 border-t-0 mb-2 sm:mb-0 hover:bg-blue-50 mb-2">
                    <td class="border-blue-900 border p-2 text-center">${t.id}</td>
                    <td class="border-blue-900 border p-2 text-center">${t.user_id} </td>
                    <td class="border-blue-900 border p-2 text-center">${date}</td>
                    <td class="border-blue-900 border p-2 text-center">Active</td>
            <td class="border-blue-900 border p-2 text-center">
                <button onclick="returnBook(${t.id })" class="text-white rounded-md font-bold px-2 hover:bg-red-600 py-1 bg-red-700">Return</button>
            </td>
                  </tr>`
          
          }).catch(function (error) {
            const data = Promise.resolve(error)
            data.then(function (data) {
                setAlert("error", data.error)
            })
        });
    }

      function selectTypeChange(id)
      {
          fetch(`/users/${id}/json`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json'
            }
          }).then(function (response)
           {
               if(response.status == 200)
               {
                   return response.json();
               }
               else
               {
                document.getElementById('details').textContent = "Wrong Member ID"
                return false;
               }
          }).then(function (data) 
          {
              if (data != false)
              {
                document.getElementById('details').textContent = data.user.name +" | Credits: " + data.user.credits
              }
          });
      }

      function returnBook(id)
      {
        fetch(`/users/return/${id}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            }
          }).then(function (response) 
          {
            if (response.ok)
            return response.json()
            else
            throw response.json()
          }).then(function (data) {
            document.getElementById(`${id}-status`).textContent = "Returned"
            document.getElementById(`${id}-return`).textContent = data.issue.returned
          }).catch(function (error) 
          {
            const data = Promise.resolve(error)
            data.then(function (data) {
                setAlert("error", data)
            })
        });
      }