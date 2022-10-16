<?php
    $file=$_POST["filePDF"];
    $output=shell_exec("submit.py"  .$file);
    echo $output;
?>