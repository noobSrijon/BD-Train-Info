from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta
app = Flask(__name__)
trains=['RANGPUR EXPRESS (771)', 'RANGPUR EXPRESS (772)', 'PANCHAGARH EXPRESS (793)', 'PANCHAGARH EXPRESS (794)', 'EKOTA EXPRESS (705)', 'EKOTA EXPRESS (706)', 'RUPSHA EXPRESS (727)', 'RUPSHA EXPRESS (728)', 'DHUMKETU EXPRESS (769)', 'DHUMKETU EXPRESS (770)', 'SIMANTA EXPRESS (747)', 'SIMANTA EXPRESS (748)', 'TUNGIPARA EXPRESS (783)', 'TUNGIPARA EXPRESS (784)', 'PADMA EXPRESS (759)', 'PADMA EXPRESS (760)', 'SILKCITY EXPRESS (753)', 'SILKCITY EXPRESS (754)', 'TITUMIR EXPRESS (733)', 'TITUMIR EXPRESS (734)', 'SIRAJGANJ EXPRESS (775)', 'SIRAJGANJ EXPRESS (776)', 'LALMONI EXPRESS (751)', 'LALMONI EXPRESS (752)', 'KURIGRAM EXPRESS (797)', 'MADHUMATI EXPRESS (755)', 'KURIGRAM EXPRESS (798)', 'MADHUMATI EXPRESS (756)', 'BARENDRA EXPRESS (731)', 'DRUTOJAN EXPRESS (757)', 'DRUTOJAN EXPRESS (758)', 'NILSAGAR EXPRESS (765)', 'CHITRA EXPRESS (763)', 'NILSAGAR EXPRESS (766)', 'CHITRA EXPRESS (764)', 'KAPOTAKSHA EXPRESS (715)', 'KAPOTAKSHA EXPRESS (716)', 'SUNDARBAN EXPRESS (725)', 'SUNDARBAN EXPRESS (726)', 'BENAPOLE EXPRESS (795)', 'BENAPOLE EXPRESS (796)', 'SAGARDARI EXPRESS (761)', 'SAGARDARI EXPRESS (762)', 'BANGLABANDHA EXPRESS (803)', 'BANGLABANDHA EXPRESS (804)', 'DHALARCHAR EXPRESS (779)', 'DHALARCHAR EXPRESS (780)', 'KOROTOA EXPRESS (713)', 'KOROTOA EXPRESS (714)', 'DOLONCHAPA EXPRESS (768)', 'DOLONCHAPA EXPRESS (767)', 'BANALATA EXPRESS (791)', 'BANALATA EXPRESS (792)', 'SONAR BANGLA EXPRESS (787)', 'SONAR BANGLA EXPRESS (788)', 'SUBORNO EXPRESS (701)', 'SUBORNO EXPRESS (702)', 'MAHANAGAR GODHULI (703)', 'MAHANAGAR PROVATI (704)', 'TISTA EXPRESS (707)', 'TISTA EXPRESS (708)', 'UPAKUL EXPRESS (711)', 'UPAKUL EXPRESS (712)', 'PARABAT EXPRESS (709)', 'PARABAT EXPRESS (710)', 'JAYENTIKA EXPRESS (717)', 'JAYENTIKA EXPRESS (718)', 'PAHARIKA EXPRESS (719)', 'PAHARIKA EXPRESS (720)', 'MOHANAGAR EXPRESS (721)', 'MOHANAGAR EXPRESS (722)', 'UDAYAN EXPRESS (723)', 'UDAYAN EXPRESS (724)', 'AGHNIBINA EXPRESS (735)', 'AGHNIBINA EXPRESS (736)', 'EGAROSINDHUR PROVATI (737)', 'EGAROSINDHUR PROVATI (738)', 'UPABAN EXPRESS (739)', 'UPABAN EXPRESS (740)', 'TURNA (741)', 'TURNA (742)', 'BHRAMMAPUTRA EXPRESS (743)', 'BHRAMMAPUTRA EXPRESS (744)', 'JAMUNA EXPRESS (745)', 'JAMUNA EXPRESS (746)', 'EGAROSINDHUR GODHULI (749)', 'EGAROSINDHUR GODHULI (750)', 'KALNI EXPRESS (773)', 'KALNI EXPRESS (774)', 'KISHORGANJ EXPRESS (781)', 'KISHORGANJ EXPRESS (782)', 'BIJOY EXPRESS (785)', 'BIJOY EXPRESS (786)', 'MOHONGANJ EXPRESS (789)', 'MOHONGANJ EXPRESS (790)', 'JAMALPUR EXPRESS (799)', 'JAMALPUR EXPRESS (800)', 'CHATTALA EXPRESS (801)', 'CHATTALA EXPRESS (802)', 'MEGHNA EXPRESS (729)', 'MEGHNA EXPRESS (730)', 'HAWR EXPRESS (777)', 'HAWR EXPRESS (778)', 'RAJSHAHI COMMUTER (57)', 'RAJSHAHI COMMUTER (58)', 'RAJSHAHI COMMUTER (77)', 'RAJSHAHI COMMUTER (78)', 'MAITREE EXPRESS (3107)', 'MAITREE EXPRESS (3110)', 'BANDHAN EXPRESS (3130)', 'MITALI EXPRESS (3131)', 'MITALI EXPRESS (3132)', 'MAITREE EXPRESS (3109)', 'MAITREE EXPRESS (3108)', 'BANDHAN EXPRESS (3129)', 'CHILAHATI EXPRESS (805)', 'CHILAHATI EXPRESS (806)', 'NARAYANGANJ COMMUTER 1 (1001)', 'NARAYANGANJ COMMUTER 2 (1002)', 'NARAYANGANJ COMMUTER 3 (1003)', 'NARAYANGANJ COMMUTER 4 (1004)', 'NARAYANGANJ COMMUTER 5 (1005)', 'NARAYANGANJ COMMUTER 6 (1006)', 'NARAYANGANJ COMMUTER 7 (1007)', 'NARAYANGANJ COMMUTER 8 (1008)', 'NARAYANGANJ COMMUTER 9 (1009)', 'NARAYANGANJ COMMUTER 10 (1010)', 'NARAYANGANJ COMMUTER 11 (1011)', 'NARAYANGANJ COMMUTER 12 (1012)', 'NARAYANGANJ COMMUTER 13 (1013)', 'NARAYANGANJ COMMUTER 14 (1014)', 'NARAYANGANJ COMMUTER 15 (1015)', 'NARAYANGANJ COMMUTER 16 (1016)', 'COXS BAZAR EXPRESS (813)', 'COXS BAZAR EXPRESS (814)', 'BURIMARI EXPRESS (809)', 'BURIMARI EXPRESS (810)', 'PARJOTAK EXPRESS (815)', 'PARJOTAK EXPRESS (816)', 'BARENDRA EXPRESS (732)', 'COX SPL 3 (003)', 'COX SPL 4 (004)', 'CHANDANA COMMUTER (121)', 'CHANDANA COMMUTER (124)', 'BHANGA COMMUTER (123)', 'BHANGA COMMUTER (122)']
def gettrain(code):
    for i in trains:
        if code in i:
            return i
    return -1
def get_train_info(trains,trip_number):
   
    for train in trains:
        if train['trip_number'] == trip_number:
            return train
    return None
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
       
        train_number = request.form['train_number']
        date_of_journey = request.form['date_of_journey']
        
        date_of_journey= datetime.strptime(date_of_journey, '%Y-%m-%d').strftime('%d-%b-%Y')

        train_name=gettrain(train_number)
        if train_name==-1:
            return 'Train Not Found'
        payload = {
            "model": train_number,
            "departure_date_time": date_of_journey  
        }
        route_response = requests.post('https://railspaapi.shohoz.com/v1.0/web/train-routes', json=payload)
        if route_response.status_code == 200:
            routes_data = route_response.json()['data']['routes']
            station_names = [route['city'] for route in routes_data]

        
            seat_availability = []
            for i in range(len(station_names) - 1):
                origin_city = station_names[0]
                destination_city = station_names[i+1]
                
                availability_url ='https://railspaapi.shohoz.com/v1.0/web/bookings/search-trips-v2?from_city={}&to_city={}&date_of_journey={}&seat_class=S_CHAIR'.format(origin_city, destination_city,date_of_journey)
                availability_response = requests.get(availability_url)
                mainurl="https://eticket.railway.gov.bd/booking/train/search?fromcity={}&tocity={}&doj={}&class=S_CHAIR".format(origin_city, destination_city,date_of_journey)
                if availability_response.status_code == 200:
                    da=availability_response.json()
                    trains = da['data']['trains']
                    data=get_train_info(trains,train_name)
                    
                    seat_types = data["seat_types"]
                    lis={}
                    info={"travel_time":data["travel_time"],'depart': data["departure_date_time"],'arrive':data["arrival_date_time"],'url':mainurl}
                    for i in seat_types:
                        lis[i['type']]={'fare':i['fare'],'seat': i["seat_counts"]['offline']+i["seat_counts"]['online']}

                    seat_availability.append([{destination_city:lis},{'info':info}])
                    
            #return seat_availability
            return render_template('result.html',origin_city = station_names[0],train_name=train_name, station_names=station_names, train_data=seat_availability)
    today = datetime.today()

    format_str = '%Y-%m-%d'

    # Print today's date in the desired format
    today_formatted = today.strftime(format_str)
    five_days_after = today + timedelta(days=4)

    # Print the date 5 days from now in the desired format
    five_days_after_formatted = five_days_after.strftime(format_str)
    return render_template('index.html',today=today_formatted,day5=five_days_after_formatted)

if __name__ == '__main__':
    app.run(debug=True)
