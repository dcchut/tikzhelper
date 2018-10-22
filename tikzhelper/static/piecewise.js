$(document).ready(function(){
    var list = document.getElementById('fn_list');

    var get_code_span = function(text) {
        var code = document.createElement('code');
        $(code).text(text);

        var span = document.createElement('span');
        $(span).html(code);

        return span;
    }

    var add_list_element = function(domain, fn, label) {
        var li = $('<li class="list-group-item d-flex"></li>');

        var div1 = $('<div class="col-md-2 p-0 fn-listentry-domain border-right"></div>');
        div1.html(get_code_span(domain));

        var div2 = $('<div class="col-md-5 pl-2 fn-listentry-fn border-right"></div>');
        div2.html(get_code_span(fn));

        var div3 = $('<div class="col-md-4 pl-2 fn-listentry-label"></div>');
        div3.html(get_code_span(label));

        var div4 = $('<div class="col-md-1 p-0"></div>');

        var button = $('<button type="button" class="close fn-listentry-delete">&times;</button>');

        div4.html(button);

        li.append(div1);
        li.append(div2);
        li.append(div3);
        li.append(div4);

        $(list).append(li);


        // hide the empty entry
        $("#fn_listentry_empty.d-flex").toggleClass('d-flex').hide();
    }

    var get_fn_list = function() {
        var domains =   [];
        var functions = [];
        var labels = [];

        $(list).children("li").not(".disabled").not("#fn_listentry_empty").each(function(idx,li){
            var domain = $(li).children("div.fn-listentry-domain").text();
            var fn = $(li).children("div.fn-listentry-fn").text();
            var label = $(li).children("div.fn-listentry-label").text();
            domains.push(domain);
            functions.push(fn);
            labels.push(label);
        });

        return {domains: domains, functions: functions, labels: labels}
    }

    var update_url = function() {
        var url = new URL(location.href);
        var fn_list = get_fn_list();
        var domains = fn_list.domains;
        var functions = fn_list.functions;
        var labels = fn_list.labels;

        if (domains.length > 0){
            url.searchParams.set('domains', JSON.stringify(domains));

        } else {
            url.searchParams.delete('domains');
        }
        if (functions.length > 0){
            url.searchParams.set('functions', JSON.stringify(functions));
        } else {
            url.searchParams.delete('functions');
        }
        if (labels.length > 0){
            url.searchParams.set('labels', JSON.stringify(labels));
        } else {
            url.searchParams.delete('labels');
        }

        history.pushState({},document.title,url.toString());
    }

    var update_hidden_vars = function() {
        var fn_list = get_fn_list();

        // update the hidden form with the domain list
        $("#fn_form_domains").val(JSON.stringify(fn_list.domains));

        // update the hidden form with the functions list
        $("#fn_form_functions").val(JSON.stringify(fn_list.functions));

        // update the hidden form with the labels list
        $("#fn_form_labels").val(JSON.stringify(fn_list.labels));
    }

    var load_from_url = function(update=true) {
        var url = new URL(location.href);
        var domains = url.searchParams.get('domains');
        var functions = url.searchParams.get('functions');
        var labels = url.searchParams.get('labels');

        if (domains !== null) {
            if (functions != null) {
                d = JSON.parse(domains);
                f = JSON.parse(functions);
                l = JSON.parse(labels);

                if (d.length == f.length && d.length == l.length) {
                    // clear the current list
                    $(list).children("li").not(".disabled").not("#fn_listentry_empty").each(function(idx,li){
                        $(li).remove();
                    });

                    for (i = 0; i < d.length; i++){
                        add_list_element(d[i],f[i], l[i]);
                    }
                }

                update_hidden_vars();

                if (update) {
                    update_url();
                }
            }
        }
    }

    $("#fn_clear").click(function(){
        $("#interval_left").val('');
        $("#interval_right").val('');
        $("#interval_type").val("(a,b)");
        $("#fn").val('');
        $("#fn_label").val('');
    });

    $("#fn_add").click(function(){
        var interval_type = $("#interval_type").val();
        var interval_left = $("#interval_left").val();
        var interval_right = $("#interval_right").val();

        var domain = ''
        var domain_l = ''
        var domain_r = ''

        // format the interval type correctly
        if (interval_type == '(a,b)') {
            domain_l = '('
            domain_r = ')'
        } else if (interval_type == '[a,b]') {
            domain_l = '['
            domain_r = ']'
        } else if (interval_type == '(a,b]') {
            domain_l = '('
            domain_r = ']'
        } else if (interval_type == '[a,b)') {
            domain_l = '['
            domain_r = ')'
        }

        // replace empty entries with +- infinity
        if (interval_left == '') {
            interval_left = '-∞';
        }
        if (interval_right == '') {
            interval_right = '∞';
        }

        // make the domain string
        domain = domain_l + interval_left + ',' + interval_right + domain_r
        fn = $("#fn").val();
        label = $("#fn_label").val();

        // only add something if there's actually something to add
        if (fn !== '' && label !== '') {
            add_list_element(domain, fn, label);

            update_hidden_vars();
            update_url();
        }
    });

    $(document).on('click', 'button.fn-listentry-delete', function(e){
        // remove the list element
        $(e.target).parents('li').remove();

        // if the list is now empty, then add an empty entry
        if ($(list).children("li").length == 2) {
            $("#fn_listentry_empty").show().toggleClass('d-flex');
        }

        update_hidden_vars();
        update_url();
    });

    // if the user presses the back/forward button, reload the list
    window.onpopstate = function(event) {
        load_from_url(false);
    }

    load_from_url(false);
});