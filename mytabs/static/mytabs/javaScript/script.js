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