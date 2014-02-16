/**
 * Created with PyCharm.
 * User: henryadam
 * Date: 9/1/13
 * Time: 6:16 PM
 * To change this template use File | Settings | File Templates.
 */
Handlebars.registerHelper('format_currency', function(amount, options) {
  if (typeof(amount) === 'string') { amount = eval(amount); }
  var rounded = Math.round(amount * 100);
  var dec = rounded % 100;
  var whole = rounded / 100 - dec / 100;
  var decStr = '' + dec;
  return '$' + whole + '.' + decStr + ( decStr.length < 2 ? '0' : '');
});

Handlebars.registerHelper('dateFormat', function(context, block) {
  if (window.moment) {
    var f = block.hash.format || "MMM Do, YYYY";
    return moment(Date(context)).format(f);
  }else{
    return context;   //  moment plugin not available. return data as is.
  };
});