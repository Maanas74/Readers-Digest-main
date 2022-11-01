function clearalert() 
{
  document.getElementById("alert").remove();
}

function setAlert(type, msg)
{
  if (type == "success")
  type = "green"
  else
  type = "red"
    
  document.getElementById("container-alerts").innerHTML = `
  <p id="alert" class="my-4 mx-1 w-1/2 right-0 fixed z-50 rounded-md font-bold text-xl bg-${type}-100 text-${type}-700 p-2">
  ${msg}
  <button
      onclick="clearalert()" class="relative float-right text-white font-bold bg-black rounded-full px-2 hover:bg-gray-700"> X
  </button>
  </p>
  `

  setTimeout(clearalert, 3000)
}