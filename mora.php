<?php
try{
$cont= new PDO("mysql:host=localhost;dbname=user;port=3306;charset=ytf8","root","");
}

catch(Exception $e){
echo "erroe is ".$e->getMessage();
}


?>