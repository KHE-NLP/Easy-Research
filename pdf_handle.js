function uploadFile() {
    var blobFile = $('#filePDF').files[0];
    var formData = new FormData();
    formData.append("data", blobFile);

    $.ajax({
       url: "147.182.183.30:12345/pdffile",
       type: "POST",
       data: formData,
       processData: false,
       contentType: false,
       success: function(response) {
            let blob = new Blob([response], { type: "*/*" });

            let a = document.createElement('a');
            a.href = window.URL.createObjectURL(blob);
            a.download = "flashread.pptx";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.removeObjectURL(a.href);
       },
       error: function(jqXHR, textStatus, errorMessage) {
           console.log(errorMessage);
       }
    });
}