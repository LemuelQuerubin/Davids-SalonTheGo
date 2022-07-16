$("#addRow").click(function () {
    var html = '';
    html += '<div id="serviceRow" class="row justify-content-between">';
    html += '<div class="col-sm-12 col-md-5 col-lg-5">';
    html += '<br>';
    html += '<select class="form-select" name="services" aria-label="Default select example" required>';
    html += '<option value="" selected disabled hidden>Select a service</option>';
    html += '<option value="Haircut">Haircut (Approx. 45 mins)</option>';
    html += '<option value="Shampoo and Blowdry">Shampoo and Blowdry</option>';
    html += '<option value="Hair Rebond">Hair Rebond (Approx. 60 mins)</option>';
    html += '<option value="Hair Relax">Hair Relax (Approx. 2 hrs)</option>';
    html += '<option value="Perm">Perm (Approx. 2 hrs)</option>';
    html += '<option value="Hair Spa">Hair Spa(Approx. 2 hrs)</option>';
    html += '<option value="Brazillian">Brazillian (Approx. 2 hrs)</option>';
    html += '<option value="Keratin">Keratin (Approx. 2 hrs)</option>';
    html += '</select>';
    html += '</div>';
    html += '<div class="col-sm-12 col-md-7 col-lg-7">';
    html += '<br>';
    html += '<i id="removeService" class="fa fa-minus-square" aria-hidden="true"></i>';
    html += '</div>';
    html += '</div>';
  
    $('#newServiceRow').append(html);
  });
  
  // remove row
  $(document).on('click', '#removeService', function () {
    $(this).closest('#serviceRow').remove();
  });