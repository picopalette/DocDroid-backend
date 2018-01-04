import pandas as pd 
import tensorflow as tf 
import numpy as np 


dataFrame = pd.read_csv('training_data.csv')
print(dataFrame)

dataFrame.loc[:,('o1')] = [1,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,0]
dataFrame.loc[:,('o2')] = dataFrame['o1'] == 0
dataFrame.loc[:,('o2')]= dataFrame['o2'].astype(int)

inputX =  dataFrame.loc[:,('time','rating')].as_matrix()
inputY =  dataFrame.loc[:,('o1','o2')].as_matrix()


learing_rate = 0.000001
training_epochs = 20000
display_step = 50
n_samples = inputY.size


x = tf.placeholder(tf.float32,[None,2])
w = tf.Variable(tf.zeros([2,2]))
b = tf.Variable(tf.zeros([2]))
y_val = tf.add(tf.matmul(x,w),b)
y = tf.nn.softmax(y_val)
y_ = tf.placeholder(tf.float32,[None,2])

error = tf.reduce_sum(tf.pow((y_ - y),2))/(n_samples)
optimizer = tf.train.GradientDescentOptimizer(learing_rate).minimize(error)

init = tf.initialize_all_variables()
saver = tf.train.Saver()
sess = tf.Session()
sess.run(init)

for i in range (training_epochs):
    sess.run(optimizer,feed_dict={x: inputX,y_ : inputY})
    if(i % display_step == 0):
        cc = sess.run(error,feed_dict={x:inputX,y_:inputY})
        print(cc)
print("finished optimization")
save_path = saver.save(sess, "G:\holmes\holmes-python\Docdroid Backend\model.ckpt")

training_error = sess.run(error,feed_dict={x:inputX,y_:inputY})
print("training error = ",training_error,"W= ", sess.run(w), "b= ", sess.run(b))


print(sess.run(y,feed_dict={x:inputX}))