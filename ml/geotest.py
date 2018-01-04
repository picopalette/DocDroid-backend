import googlemaps
import json
import tensorflow as tf 
import numpy as np 


x = tf.placeholder(tf.float32,[None,2])
w = tf.Variable(tf.zeros([2,2]))
b = tf.Variable(tf.zeros([2]))
y_val = tf.add(tf.matmul(x,w),b)
y = tf.nn.softmax(y_val)

gmaps = googlemaps.Client(key="AIzaSyCThwYhTx35MT4_LRUxLC_GnvfE-RPA67c")

result = gmaps.places("hospital", location="13.1067,80.0970", radius=5000, language=None,
           min_price=None, max_price=None, open_now=True, type=None,
           page_token=None)

unrated_hospitals = []
hospital_names = []
hospital_ratings=[]
travel_time=[]

for ratings in result["results"]:
    if ratings.get("rating"):
        #print(ratings["rating"])
        #print("\n")
        #print(ratings['geometry']['location'])
        hospital_names.append(ratings['formatted_address'])
        hospital_ratings.append(ratings['rating'])      
    else:
        unrated_hospitals.append(ratings['formatted_address'])

route = gmaps.distance_matrix(origins="13.1067,80.0970", destinations=hospital_names,
                    mode="driving", language=None, avoid=None, units=None,
                    departure_time=None, arrival_time=None, transit_mode=None,
                    transit_routing_preference=None, traffic_model=None)

        
for times in route['rows'][0]['elements']:
    travel_time.append((times['duration']['text']).split(" ")[0])

#for i in range(len(hospital_ratings)):
#    print(hospital_ratings[i], travel_time[i])

myinput =  np.column_stack((travel_time,hospital_ratings))

print(myinput)

init = tf.global_variables_initializer()
saver = tf.train.Saver()
sess = tf.Session()
sess.run(init)

saver.restore(sess, "G:\holmes\holmes-python\Docdroid Backend\model.ckpt")


final_result = sess.run(y,feed_dict={x:myinput})
print(final_result)