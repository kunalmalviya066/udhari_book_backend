// 🔹 User Login
function login() {
    let mobile = document.getElementById('mobile').value;
    let password = document.getElementById('password').value;

    fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mobile, password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.token) {
            localStorage.setItem("token", data.token);
            window.location.href = "dashboard.html";
        } else {
            alert("Invalid credentials");
        }
    });
}

// 🔹 User Registration
function register() {
    let mobile = document.getElementById('reg_mobile').value;
    let password = document.getElementById('reg_password').value;

    fetch("http://127.0.0.1:5000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mobile, password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.message) {
            alert("Registration Successful! Please login.");
            window.location.href = "index.html";
        } else {
            alert(data.error);
        }
    });
}

// 🔹 Logout
function logout() {
    localStorage.removeItem("token");
    window.location.href = "index.html";
}

// 🔹 Add Customer
function addCustomer() {
    let name = document.getElementById('name').value;
    let mobile = document.getElementById('customer_mobile').value;
    let balance = document.getElementById('balance').value;
    let token = localStorage.getItem("token");

    fetch("http://127.0.0.1:5000/add_customer", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({ name, mobile, balance })
    })
    .then(res => res.json())
    .then(data => {
        if (data.message) {
            alert("Customer Added!");
            location.reload();
        }
    });
}

// 🔹 Get Customers
function getCustomers() {
    let token = localStorage.getItem("token");

    fetch("http://127.0.0.1:5000/customers", {
        headers: { "Authorization": "Bearer " + token }
    })
    .then(res => res.json())
    .then(customers => {
        let table = document.getElementById("customerTable");
        table.innerHTML = "";
        customers.forEach(c => {
            table.innerHTML += `<tr><td>${c.name}</td><td>${c.mobile}</td><td>${c.balance}</td></tr>`;
        });
    });
}
