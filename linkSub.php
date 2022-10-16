<?php
    $file=$_POST["urlPDF"];
    $output=shell_exec("submit.py"  .$file);
    echo $output;
?>