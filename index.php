<?php
session_start();
include 'inc/config.php';

if(isset($_POST['submit'])){
    $user = $_POST['email'];
    $password = md5($_POST['password']);
    $role = $_POST['role']; // either 'admin' or 'staff'

    $sql = "SELECT * FROM users WHERE email='$user' AND password='$password' AND role='$role'";
    $run = mysqli_query($con,$sql);
    $check = mysqli_num_rows($run);

    if($check == 1){
        $_SESSION['email'] = $user;
        $_SESSION['role'] = $role;

        if($role == 'admin'){
            header("Location: admin_dashboard.php");
        } else {
            header("Location: staff_dashboard.php");
        }
        exit();
    } else {
        echo "<script>alert('Email or Password Invalid');</script>";
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Online Leave Management</title>
    <link rel="stylesheet" href="css/bootstrap.css">
    <link rel="stylesheet" href="css/font-awesome.min.css">
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
<div class="container text-center mt-5">
    <h2>Online Leave Management System</h2>

    <form method="POST" class="mt-4">
        <label>Email:</label><br>
        <input type="email" name="email" class="form-control mb-2" required>

        <label>Password:</label><br>
        <input type="password" name="password" class="form-control mb-2" required>

        <label>Login as:</label><br>
        <select name="role" class="form-control mb-3" required>
            <option value="">Select Role</option>
            <option value="staff">Staff</option>
            <option value="admin">Admin</option>
        </select>

        <input type="submit" name="submit" class="btn btn-primary" value="Log In">
    </form>
</div>
</body>
</html>
