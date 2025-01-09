
var documents = [{
    "id": 0,
    "url": "/404.html",
    "title": "404",
    "body": "404 Page does not exist!Please use the search bar at the top or visit our homepage! "
    }, {
    "id": 1,
    "url": "/about",
    "title": "Little About Me",
    "body": " DescriptionI’m Adam Holmes, a food blogger based in Southern California. My blog blends photos, reviews, and personal stories, highlighting every unique spot I visit. Exploring new flavors and sharing those experiences with my audience keeps those moments alive. Outside of food blogging, I enjoy starting my mornings with a bike ride, and on Wednesdays, I stop by the farmer’s market before work. For me, food isn’t just about nourishment—it’s an experience that creates memorable moments and connections.  "
    }, {
    "id": 2,
    "url": "/categories",
    "title": "Categories",
    "body": ""
    }, {
    "id": 3,
    "url": "/",
    "title": "Home",
    "body": "      Featured:                                                                                                                                                                                                                 Pizza by The Water                                                 1 2 3 4 5                                              :               We took our annual road trip to Baja California Sur to visit the beach and play some golf. I like how this location is farther. . . :                                                                                                                                                                                                       20 Dec 2023                                                                                                                                                                                                                                                                                                                              Berry Berry at Beignet Spot                                                 1 2 3 4 5                                              :               It was bum hot outside, so I decided to cool off at a beignet spot after a business meeting. Since it was mid-afternoon, the place. . . :                                                                                                                                                                                                       20 Jun 2023                                                                                                                                                                                                                                                                                                                              Pork Cutlet                                                 1 2 3 4 5                                              :               My friend introduced me to their favorite local restaurant. It was my first time having a pork cutlet served in a pan. The sauce made. . . :                                                                                                                                                                                                       23 Apr 2021                                                                                                                                                                                                                                                                                                                        Airport Ramen at IPPUDO Narita Airport                                                 1 2 3 4 5                                              :               I didn’t eat much on the plane. Airplane food has always left a pit in my stomach. I usually eat before my flight or buy. . . :                                                                                                                                                                                                       20 Apr 2021                                                                                                                            All Stories:                                                                                                     Pizza by The Water                         1 2 3 4 5                      :       We took our annual road trip to Baja California Sur to visit the beach and play some golf. I like how this location is farther from the city compared to. . . :                                                                                               20 Dec 2023                                                                                                                                     Chicken Alfredo at Marmalade Cafe                         1 2 3 4 5                      :       I was in the area and decided to try this café chain since I’d heard a lot about it. The atmosphere felt a bit dull, and the floor looked like. . . :                                                                                               02 Sep 2023                                                                                                                                     Peking Duck Salad at MOT 32                         1 2 3 4 5                      :       I don’t usually like spending time in the casino because cigarette smoke tends to trigger my allergies. :                                                                                               21 Aug 2023                                                                                                                                     Berry Berry at Beignet Spot                         1 2 3 4 5                      :       It was bum hot outside, so I decided to cool off at a beignet spot after a business meeting. Since it was mid-afternoon, the place was nearly empty. :                                                                                               20 Jun 2023                                                                                                                                     Beef Bowl Noodles at Bowltiful Lanzhou                         1 2 3 4 5                      :       I arrived to Melbourne pretty late and most restaurants were closed. But Bowltiful was open and I was pleasantly surprised by the flavor of the chili and noodles. Since it. . . :                                                                                               10 Sep 2021                                                                                                                                     Not Eelaborate                         1 2 3 4 5                      :       After my long train ride, I visited a deer park and got to feed the wildlife. There were so many restaurants to choose from but I was craving eel. I. . . :                                                                                               25 Apr 2021                                        		       &laquo; Prev       1        2      Next &raquo; "
    }, {
    "id": 4,
    "url": "/robots.txt",
    "title": "",
    "body": "      Sitemap: {{ &#8220;sitemap. xml&#8221;   absolute_url }}   "
    }, {
    "id": 5,
    "url": "/page2/",
    "title": "Home",
    "body": "{% if page. url == “/” %}       Featured:       {% for post in site. posts %}    {% if post. featured == true %}      {% include featuredbox. html %}    {% endif %}  {% endfor %}  {% endif %}       All Stories:         {% for post in paginator. posts %}    {% include postbox. html %}    {% endfor %}		    {% include pagination. html %}"
    }, {
    "id": 6,
    "url": "/late-night-bite/",
    "title": "Late Night Bite",
    "body": "2025/01/02 - Some nights, I enjoy walking out to this modern local izakaya restaurant. They close pretty late, which makes it perfect for a late night snack. What makes this place unique is their dedication to brewing their own teas and constantly experimenting with new dishes on the menu. I like to order their mocktail Shiso Dry as my drink. As for meal spicy tuna onigiri with a bowl of miso soup is enough for me. I just want to show my appreciation and admiration for this place. But you guys will never find it! I regularly come here during the weekends. "
    }, {
    "id": 7,
    "url": "/pizza-by-the-water/",
    "title": "Pizza by The Water",
    "body": "2023/12/20 - We took our annual road trip to Baja California Sur to visit the beach and play some golf. I like how this location is farther from the city compared to other resorts. I really enjoyed the sweet and savory sauce on the pizza with shredded chicken. After eating, I fell asleep, and half of my legs ended up getting tanned. "
    }, {
    "id": 8,
    "url": "/chicken-alfredo-at-marmalade-cafe/",
    "title": "Chicken Alfredo at Marmalade Cafe",
    "body": "2023/09/02 - I was in the area and decided to try this café chain since I’d heard a lot about it. The atmosphere felt a bit dull, and the floor looked like it hadn’t been swept in a while, but it might have just been a temporary lapse. The food took a little longer than expected, but I didn’t mind since I was nursing my orange juice while waiting. The portion size was reasonable, and I appreciated the sauce’s consistency. However, I was disappointed by how dry the chicken was. "
    }, {
    "id": 9,
    "url": "/peking-duck-salat-at-mot-32/",
    "title": "Peking Duck Salad at MOT 32",
    "body": "2023/08/21 - I don’t usually like spending time in the casino because cigarette smoke tends to trigger my allergies. The Peking duck salad was quite good—I especially enjoyed the dressing and fresh vegetables paired with the duck. The price of the salad is debatable, given that they used a citrus truffle dressing. While I thought it was good, it’s not something I’d go out of my way to eat again. There’s also a business casual dress code, which I understand, but it’s not exactly a place I’d choose to dine alone again. "
    }, {
    "id": 10,
    "url": "/berry-berry-at-beignet-spot/",
    "title": "Berry Berry at Beignet Spot",
    "body": "2023/06/20 - It was bum hot outside, so I decided to cool off at a beignet spot after a business meeting. Since it was mid-afternoon, the place was nearly empty. The cashier greeted me warmly as I walked in, and I ordered the Berry Berry. While waiting, I peered through a large window into the kitchen to watch the beignets being made. When my order arrived, I was surprised by the large portion size. The assortment of berries and the generous amount of jam were delightful. Although the whipped cream was a bit much on my sweet tooth, it still paired well with the beignets. Thankfully, there was a water station nearby, which helped washed out the sweetness. I wouldn’t come back alone, but I’d definitely return with a friend to share the portions with. "
    }, {
    "id": 11,
    "url": "/beef-bowl-noodles-at-bowltiful-lanzhou/",
    "title": "Beef Bowl Noodles at Bowltiful Lanzhou",
    "body": "2021/09/10 - I arrived to Melbourne pretty late and most restaurants were closed. But Bowltiful was open and I was pleasantly surprised by the flavor of the chili and noodles. Since it was rather late, it allowed me to enjoy the atmosphere of the place. "
    }, {
    "id": 12,
    "url": "/not-elaborate/",
    "title": "Not Eelaborate",
    "body": "2021/04/25 - After my long train ride, I visited a deer park and got to feed the wildlife. There were so many restaurants to choose from but I was craving eel. I really like the soup mixed in with the rice and fish. The wasabi threw me off since I don’t normally have it served this way. I would recommend this place if you want to find a quiet restaurant to eat at, and wouldn’t mind finding a few small fish bones. Eels are known to carry lots of tiny bones it’s inevitable that you’ll find it in a lot of places. "
    }, {
    "id": 13,
    "url": "/pork-cutlet/",
    "title": "Pork Cutlet",
    "body": "2021/04/23 - My friend introduced me to their favorite local restaurant. It was my first time having a pork cutlet served in a pan. The sauce made it slightly soggy, but the tangy, savory flavor was banger. I was really happy with the meal, and I’d love to try a different item on the menu next time. "
    }, {
    "id": 14,
    "url": "/sleuths-and-sweets/",
    "title": "Sleuths and Sweets",
    "body": "2021/04/21 - I visited my friend in Japan, and we had some decent crepes! The area was bustling with foot traffic, so we expected a long wait, but it ended up being okay. I’m usually not a fan of yogurt in my crepes, but I was content with it. Finding a seat was difficult because the place was crowded, and walking elsewhere to eat wasn’t an option, as it’s culturally considered rude to eat while walking in Japan.  "
    }, {
    "id": 15,
    "url": "/airport-ramen-at-ippudo-narita-airport/",
    "title": "Airport Ramen at IPPUDO Narita Airport",
    "body": "2021/04/20 - I didn’t eat much on the plane. Airplane food has always left a pit in my stomach. I usually eat before my flight or buy a couple of sandwiches before I board. But this ramen tasted so good. I don’t know if I was just hungry, but I slurped that noodle and downed the broth. It was really hard to find a place to sit and it was uncomfortably packed. It would be nice if the restaurant could move to a bigger space to accommodate for luggage and seating space. I don’t feel uncomfortable having my luggage outside the restaurant. "
    }, {
    "id": 16,
    "url": "/penne-pasta-at-caffe-dante/",
    "title": "Penne Pasta at Caffe Dante",
    "body": "2019/08/07 - I enjoyed the flavor of the penne pasta from Caffe Dante, but I wish they had added more sauce—it felt like they skimped on it. We also fell for a tourist trap. My friend wanted to try their regular-sized mocktail, but the waiter claimed it was too small. She ended up ordering the extra-large size and was charged €30. We should’ve checked the menu and canceled the drink, but honestly, who charges that much for a mocktail?. ” "
    }];

var idx = lunr(function () {
    this.ref('id')
    this.field('title')
    this.field('body')

    documents.forEach(function (doc) {
        this.add(doc)
    }, this)
});
function lunr_search(term) {
    document.getElementById('lunrsearchresults').innerHTML = '<ul></ul>';
    if(term) {
        document.getElementById('lunrsearchresults').innerHTML = "<p>Search results for '" + term + "'</p>" + document.getElementById('lunrsearchresults').innerHTML;
        //put results on the screen.
        var results = idx.search(term);
        if(results.length>0){
            //console.log(idx.search(term));
            //if results
            for (var i = 0; i < results.length; i++) {
                // more statements
                var ref = results[i]['ref'];
                var url = documents[ref]['url'];
                var title = documents[ref]['title'];
                var body = documents[ref]['body'].substring(0,160)+'...';
                document.querySelectorAll('#lunrsearchresults ul')[0].innerHTML = document.querySelectorAll('#lunrsearchresults ul')[0].innerHTML + "<li class='lunrsearchresult'><a href='" + url + "'><span class='title'>" + title + "</span><br /><span class='body'>"+ body +"</span><br /><span class='url'>"+ url +"</span></a></li>";
            }
        } else {
            document.querySelectorAll('#lunrsearchresults ul')[0].innerHTML = "<li class='lunrsearchresult'>No results found...</li>";
        }
    }
    return false;
}

function lunr_search(term) {
    $('#lunrsearchresults').show( 400 );
    $( "body" ).addClass( "modal-open" );
    
    document.getElementById('lunrsearchresults').innerHTML = '<div id="resultsmodal" class="modal fade show d-block"  tabindex="-1" role="dialog" aria-labelledby="resultsmodal"> <div class="modal-dialog shadow-lg" role="document"> <div class="modal-content"> <div class="modal-header" id="modtit"> <button type="button" class="close" id="btnx" data-dismiss="modal" aria-label="Close"> &times; </button> </div> <div class="modal-body"> <ul class="mb-0"> </ul>    </div> <div class="modal-footer"><button id="btnx" type="button" class="btn btn-danger btn-sm" data-dismiss="modal">Close</button></div></div> </div></div>';
    if(term) {
        document.getElementById('modtit').innerHTML = "<h5 class='modal-title'>Search results for '" + term + "'</h5>" + document.getElementById('modtit').innerHTML;
        //put results on the screen.
        var results = idx.search(term);
        if(results.length>0){
            //console.log(idx.search(term));
            //if results
            for (var i = 0; i < results.length; i++) {
                // more statements
                var ref = results[i]['ref'];
                var url = documents[ref]['url'];
                var title = documents[ref]['title'];
                var body = documents[ref]['body'].substring(0,160)+'...';
                document.querySelectorAll('#lunrsearchresults ul')[0].innerHTML = document.querySelectorAll('#lunrsearchresults ul')[0].innerHTML + "<li class='lunrsearchresult'><a href='" + url + "'><span class='title'>" + title + "</span><br /><small><span class='body'>"+ body +"</span><br /><span class='url'>"+ url +"</span></small></a></li>";
            }
        } else {
            document.querySelectorAll('#lunrsearchresults ul')[0].innerHTML = "<li class='lunrsearchresult'>Sorry, no results found. Close & try a different search!</li>";
        }
    }
    return false;
}
    
$(function() {
    $("#lunrsearchresults").on('click', '#btnx', function () {
        $('#lunrsearchresults').hide( 5 );
        $( "body" ).removeClass( "modal-open" );
    });
});