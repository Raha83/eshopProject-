function sendArticleComment(articleId) {
    var comment = $('#commentText').val();
    var parentId = $('#parent_id').val();
    $.get('/articles/article-add-comment', {
        article_comment: comment,
        article_id: articleId,
        parent_id: parentId
    }).then(res => {
        $('#comments_area').html(res);
        $('#commentText').val('');
        $('#parent_id').val('');
        if (parentId !== null && parentId !== '') {
            document.getElementById('single_comment_' + parentId).scrollIntoView({ behavior: "smooth" });
        } else {
            document.getElementById('comments_area').scrollIntoView({ behavior: "smooth" });
        }

    });
}

function fillParentId(parentId) {
    $('#parent_id').val(parentId);
    document.getElementById('commentBox').scrollIntoView({ behavior: 'smooth' });
}

function filterProduct() {
    const filterPrice = $('#sl2').val();
    const start_price = filterPrice.split(',')[0];
    const end_price = filterPrice.split(',')[1];
    $('#start_price').val(start_price);
    $('#end_price').val(end_price);
    $('#filter_form').submit();
}

function fillPage(pageNumber) {
    $('#page_number').val(pageNumber);
    $("#filter_form").submit();
}

function ShowLargeImage(imageSrc) {
    $('#main_image').attr('src', imageSrc);
    $('#show_large_image').attr('href', imageSrc);
}

function addProductToOrder(productId) {
    const productCount = $('#productCount').val();
    $.get('/order/add-to-cart?product_id=' + productId + '&product_count=' + productCount).then(res => {
        Swal.fire({
            title: "اعلان",
            text: res.text,
            icon: res.icon,
            showCancelButton: false,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: res.confirm_button_text
        }).then((result) => {
            if (result.isConfirmed && res.status === 'not_auth'){
                window.location.href='/login';
            }else if (result.isConfirmed && res.status === 'success'){
                window.location.href='/user/user-basket';
            };
          });
    });
}

function remove_order_item(detailId){
    $.get('/user/user-order-remove?detail_id='+detailId).then(res => {
        if (res.status === 'success'){
            $('#order-detail-content').html(res.body);
        }
    });
}

function order_detail_quantity(detailId,state){
    $.get('/user/user-order-quantity?detail_id='+detailId+ '&state='+state).then(res => {
        if (res.status === 'success'){
            $('#order-detail-content').html(res.body);
        }
    })
}


