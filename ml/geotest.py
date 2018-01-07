import googlemaps
import json
import tensorflow as tf 
import numpy as np 


def predictHospital(loc):
    x = tf.placeholder(tf.float32,[None,2])
    w = tf.Variable(tf.zeros([2,2]))
    b = tf.Variable(tf.zeros([2]))
    y_val = tf.add(tf.matmul(x,w),b)
    y = tf.nn.softmax(y_val)

    gmaps = googlemaps.Client(key="AIzaSyDnCGt9WkPVZ_D0C-dPPs4JjKs20ufwkU0")

    result = gmaps.places("hospital", location=loc, radius=5000, language=None,
               min_price=None, max_price=None, open_now=True, type=None,
               page_token=None)

    #print(result['results'])

    unrated_hospitals = []
    hospital_addrs=[]
    hospital_names = []
    hospital_ratings=[]
    travel_time=[]
    hospital_locs=[]

    for ratings in result["results"]:
        if ratings.get("rating"):
            #print(ratings["rating"])
            #print("\n")
            #print(ratings['geometry']['location'])
            hospital_names.append(ratings['name'])
            hospital_addrs.append(ratings['formatted_address'])
            hospital_ratings.append(ratings['rating'])
            hospital_locs.append(ratings['geometry']['location'])      
        else:
            unrated_hospitals.append(ratings['formatted_address'])

    route = gmaps.distance_matrix(origins=loc, destinations=hospital_addrs,
                        mode="driving", language=None, avoid=None, units=None,
                        departure_time=None, arrival_time=None, transit_mode=None,
                        transit_routing_preference=None, traffic_model=None)


    for index, times in enumerate(route['rows'][0]['elements']):
        if times['status'] == 'OK':
            #print(times)
            travel_time.append((times['duration']['text']).split(" ")[0])
        else:
            del hospital_names[index]
            del hospital_addrs[index]
            del hospital_ratings[index]
            del hospital_locs[index]

    #for i in range(len(hospital_ratings)):
    #    print(hospital_ratings[i], travel_time[i])
    #print(hospital_names,hospital_addrs,hospital_ratings,hospital_locs)

    myinput =  np.column_stack((travel_time,hospital_ratings))

    #print(myinput)

    init = tf.global_variables_initializer()
    saver = tf.train.Saver()
    sess = tf.Session()
    sess.run(init)

    saver.restore(sess, "./ml/model.ckpt")


    final_result = sess.run(y,feed_dict={x:myinput})
    ans = [row[0] for row in final_result]
    hosp_index = ans.index(max(ans))
    ans = dict()
    ans['lat'] = str(hospital_locs[hosp_index]['lat'])
    ans['log'] = str(hospital_locs[hosp_index]['lng'])

    return ans
    #print(hosp_index)
    #print(hospital_names[hosp_index], hospital_addrs[hosp_index], hospital_ratings[hosp_index], travel_time[hosp_index], hospital_locs[hosp_index])

if __name__ == "__main__":
    print(predictHospital("12.9230363,77.4988752"))