window.onload = function () {
    let _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_sum;

    const quantity_arr = [];
    const price_arr = [];

    const TOTAL_FORMS = parseInt($('input[name=orderitems-TOTAL_FORMS]').val());

    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    let order_total_sum = parseFloat($('.order_total_sum').text().replace(',', '.')) || 0;

    for (let i = 0; i < TOTAL_FORMS; i++) {
        _quantity = parseInt($('input[name=orderitems-' + i + '-quantity]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));

        quantity_arr[i] = _quantity;
        if (_price) {
            price_arr[i] = _price;
        } else {
            price_arr[i] = 0;
        }

    }
    $('.card').on('click', 'input[type=number]', function () {
        const target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (price_arr[orderitem_num]) {
            orderitem_quantity = parseInt(target.value);
            console.log(orderitem_quantity)
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            quantity_arr[orderitem_num] = orderitem_quantity;
            orderSummeryUpdate(price_arr[orderitem_num], delta_quantity)
        }
    });

    $('.card').on('click', 'input[type=checkbox]', function () {
        const target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (target.checked) {
            delta_quantity = -quantity_arr[orderitem_num];
        } else {
            delta_quantity = quantity_arr[orderitem_num];
        }
        orderSummeryUpdate(price_arr[orderitem_num], delta_quantity)
    });

    function orderSummeryUpdate(orderitem_price, delta_quantity) {
        delta_sum = orderitem_price * delta_quantity;

        order_total_sum = Number((order_total_sum + delta_sum).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;

        $('.order_total_quantity').html(order_total_quantity);
        $('.order_total_sum').html(order_total_sum);
    }

    $('.formset_row').formset({
        addText: 'Добавить товар',
        deleteText: 'Удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem

    });

    function deleteOrderItem(row) {
        var target_name = row[0].querySelector('input[type=number]').name;
        orderitem_num = target_name.replace('orderitems-', '').replace('-quantity', '');
        delta_quantity = -quantity_arr[orderitem_num];
        orderSummeryUpdate(price_arr[orderitem_num], delta_quantity)
    }
}