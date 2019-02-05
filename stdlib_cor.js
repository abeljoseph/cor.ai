module.exports = async (palp = "", bmi = "", excmin = "", chol = "") => {
  var bigString = "";

var gpalp, gbmiLower, gbmiUpper, gexcmin, gchol;
var length = 2;

gpalp = 30;
gbmiLower = 19;
gbmiUpper = 24;
gexcmin = 75;
gchol = 170;

good_palp(palp, gpalp);
good_bmi(bmi, gbmiUpper, gbmiLower);
good_excmin(excmin, gexcmin);
good_chol(chol, gchol);

function good_palp (palp, gpalp) {
  if (palp > gpalp) {
    var pl = palp - gpalp;
    bigString = bigString + ("Heart palpitations are " + pl + " palpitations too high");
  } else if (palp == gpalp) {
    bigString = bigString + "Heart palpitations are almost at level of risk";
  } else {
    bigString = bigString + "Heart palpitations are normal";
  }
}

function good_bmi (bmi, gbmiUpper, gbmiLower) {
  if (bmi >= gbmiLower && bmi <= gbmiUpper) {
    bigString = bigString + ", Your BMI is normal";
  } else if (bmi < gbmiLower) {
    bigString = bigString + ", Your BMI is lower than normal";
  } else {
    bigString = bigString + ", Your BMI is higher than normal";
  }
}

function good_excmin (excmin, gexcmin){
  if (excmin < gexcmin) {
    var ex = (((gexcmin - excmin)/ gexcmin) * 100);
    var tr_ex = ex | 0;
    bigString = bigString + ", Your minutes of exercise per week is " + tr_ex + "% lower than normal";
  } else {
    bigString = bigString + ", Your minutes of exercise per week are better than normal";
  }
}

function good_chol (chol, gchol) {
  if (chol > gchol) {
    var ch = (((chol - gchol)/ gchol) * 100);
    var tr_ch = ch | 0;
    bigString = bigString + ", Your cholesterol levels are " + tr_ch + "% higher than normal";
  } else {
    bigString = bigString + ", Your cholesterol levels are good";
  }
}
return bigString;
};