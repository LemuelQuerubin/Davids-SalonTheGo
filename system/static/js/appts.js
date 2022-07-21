$("#addRow").click(function () {
    var html = '';
    html += '<div id="serviceRow" class="row justify-content-between">';
    html += '<div class="col-sm-12 col-md-5 col-lg-5">';
    html += '<br>';
    html += '<select class="form-select" name="services" aria-label="Default select example" required>';
    html += '<option value="" selected disabled hidden>Select a service</option>';
    // HAIRCUT
    html += '<option value="Haircut">Haircut (₱350)</option>';
    //COLOR
    html += '<option value="Tint">Tint (₱1,750)</option>';
    html += '<option value="Cellophane">Cellophane (₱1,960)</option>';
    html += '<option value="Highlights">Highlights (foil) (₱2,240)</option>';
    // TREATMENT
    html += '<option value="Regular Hot Oil">Regular Hot Oil(₱980)</option>';
    html += '<option value="Hair Spa">Hair Spa (₱1,400)</option>';
    html += '<option value="Intense Treatment">Intense Treatment (₱1,680)</option>';
    html += '<option value="Keratin">Keratin (₱4,500)</option>';
    html += '<option value="Brazillian">Brazillian (₱4,500)</option>';
    // FORM
    html += '<option value="Perm">Perm (₱2,100)</option>';
    html += '<option value="Hair Relax">Hair Relax (₱3,360)</option>';
    html += '<option value="Hair Rebond">Hair Rebond (₱4,500)</option>';
    // HAIR AND MAKE UP
    html += '<option value="Shampoo and Blowdry">Shampoo and Blowdry (₱300)</option>';
    html += '<option value="Setting Ironing">Setting/Ironing (₱600)</option>';
    html += '<option value="Make-up">Make-up (₱1,120)</option>';
    html += '<option value="Hair & Make-up">Hair & Make-up (₱1,500)</option>';
   /*
    // THREADING
    html += '<option value="Eyebrow">Eyebrow (₱225)</option>';
    html += '<option value="Eyebrow(Shave)">Eyebrow(Shave) (₱150)</option>';
    html += '<option value="Upper Lip">Upper Lip (₱225)</option>';
    html += '<option value="Full Face">Full Face (₱650)</option>';

    // NAIL CARE
    html += '<option value="Manicure">Manicure (₱250)</option>';
    html += '<option value="Pedicure">Pedicure (₱310)</option>';
    html += '<option value="Foot Spa"> Foot Spa (₱350)</option>';
    html += '<option value="Foot Massage">Foot Massage (₱350)</option>';
    html += '<option value="Nail Gel">Nail Gel (₱300)</option>';
    html += '<option value="Nail Gel Removal">Nail Gel Removal (₱180)</option>';
    html += '<option value="Pedicure">Change Polish (₱200)</option>';
  */
    
    
    
    
   
    
    
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

  // service - price
  // total approximate time

  // DISABLE SAME OPTION FROM BEING PICKED
  /*
    $('select[name=services]').on('change', function() {
      var self = this;
      $('select[name=services]').find('option').prop('disabled', function() {
          return this.value == self.value
      });
  });
  */