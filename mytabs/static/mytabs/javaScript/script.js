function handleModal() {
	console.log("handleModal()")
    // Get the modal
    var modal = document.getElementById("myModal");
    
    // Get the button that opens the modal
    var btn = document.getElementById("myBtn");
    
    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];
    
    // When the user clicks the button, open the modal 
    btn.onclick = function() {
      modal.style.display = "block";
    }
    
    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
      modal.style.display = "none";
    }
    
    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    }
   
}



function sideBarNav() {
	var x = document.getElementById("mySideBar");
	var y = document.getElementById("main");
	var z = document.getElementById("sideBarButton");
	var a = "500px"
	console.log("2");
	// if (typeof(Storage) !== "undefined") {
	// 	console.log("open")
    //     // Save the state of the sidebar as "open"
    //     localStorage.setItem("sidebar", "opened");
    // }else{
	// 	console.log("no storage")
	// }
	if (z.innerHTML === "☰") {
		if (typeof(Storage) !== "undefined") {
			console.log("open")
			// Save the state of the sidebar as "open"
			localStorage.setItem("sidebar", "opened");
		}else{
			console.log("no storage")
		}
		x.style.width = a;
		y.style.marginLeft = a;
		z.innerHTML = "X";
	}
	else {
		if (typeof(Storage) !== "undefined") {
			console.log("open")
			// Save the state of the sidebar as "open"
			localStorage.setItem("sidebar", "closed");
		}else{
			console.log("no storage")
		}
		x.style.width = "0px";
		y.style.marginLeft = "0px";
		z.innerHTML = "☰";
	}
}