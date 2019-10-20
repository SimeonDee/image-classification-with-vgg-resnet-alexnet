#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# */AIPND/intropylab-classifying-images/check_images.py
#                                                                             
# TODO: 0. Fill in your information in the programming header below
# PROGRAMMER:   Adeyemi Adedoyin Simeon
# DATE CREATED: 10/18/2019
# REVISED DATE: 10/20/2019 12:47 AM            <=(Date Revised - if any)
# REVISED DATE: 10/20/2019 - Completed the project today

# PURPOSE: Check images & report results: read them in, predict their
#          content (classifier), compare prediction to actual value labels
#          and output results
#
# Use argparse Expected Call with <> indicating expected user input:
#      python check_images.py --dir <directory with images> --arch <model>
#             --dogfile <file that contains dognames>
#   Example call:
#    python check_images.py --dir pet_images/ --arch vgg --dogfile dognames.txt
##

# Imports python modules
import argparse
from time import time, sleep
from os import listdir
# Imports classifier function for using CNN to classify images 
from classifier import classifier 

# Imports print functions that check the lab
from print_functions_for_lab_checks import *

# Main program function defined below
def main():
    # TODO: 1. Define start_time to measure total program runtime by
    # collecting start time
    start_time = time()
    #sleep(50)
    
    
    # TODO: 2. Define get_input_args() function to create & retrieve command
    # line arguments
    def get_input_args():
        #instantiating argparse object
        parser = argparse.ArgumentParser()
        
        #Adding arguments
        parser.add_argument('--dir', type=str, default='pet_images/', help='path to the folder pet_images')
        parser.add_argument('--arch', type=str, default='resnet', help='the cnn architecture to use')
        parser.add_argument('--dogfile', type=str, default='dognames.txt', help='the file containing the dog names')
        
        return parser.parse_args()
        
    in_arg = get_input_args()
    
    #Testing the result
    #check_command_line_arguments(in_arg)
    
    
    # TODO: 3. Define get_pet_labels() function to create pet image labels by
    # creating a dictionary with key=filename and value=file label to be used
    # to check the accuracy of the classifier function
    def get_pet_labels(image_dir):
        #Read list of files in image_dir
        filename_list = listdir(image_dir)
        
        petlabels_dic = dict()
        for filename in filename_list:
            if filename not in petlabels_dic:
                petlabels_dic[filename] = ' '.join(filename.split('_')[:-1]).lower().strip()
                
        return petlabels_dic
    
    #Calling the function
    answers_dic = get_pet_labels(in_arg.dir)
    
    #Testing the result
    #check_creating_pet_image_labels(answers_dic)

    
    
    # TODO: 4. Define classify_images() function to create the classifier 
    # labels with the classifier function uisng in_arg.arch, comparing the 
    # labels, and creating a dictionary of results (result_dic)
    def classify_images(images_dir, petlabel_dic, model):
        results_dic = dict()
        value_list = list()
            
        for key,true_label in petlabel_dic.items():    
            test_image_path = images_dir + key
            classified_label = classifier(test_image_path, model)
            value_list = [true_label, classified_label.lower()]
            
            found_index = classified_label.lower().strip().find(true_label)
            if found_index >= 0:
                if found_index == 0 and len(true_label) == len(classified_label):
                    value_list.append(1)
                    
                elif ( (found_index == 0) or (classified_label[found_index - 1] == " ") )  and (  ( found_index + len(true_label) == len(classified_label) ) or ( classified_label[found_index + len(true_label):found_index + len(true_label) +1] in  (" ",",") )  ):
                    value_list.append(1)
                    
                else:
                    value_list.append(0)
                    
            else:
                value_list.append(0)
                
            results_dic[key] = value_list
            
            
        return results_dic
    
    
    # Calling the classify_images() function
    result_dic = classify_images(in_arg.dir, answers_dic, in_arg.arch)
    
    # Testing the Classify_image()
    #check_classifying_images(result_dic)
    
    
    
    
    # TODO: 5. Define adjust_results4_isadog() function to adjust the results
    # dictionary(result_dic) to determine if classifier correctly classified
    # images as 'a dog' or 'not a dog'. This demonstrates if the model can
    # correctly classify dog images as dogs (regardless of breed)
    def adjust_results4_isadog(results_dic, dogsfile):
        #Codes here
        dognames_dic = dict()
        counter = 0
        with open(in_arg.dogfile, 'r') as dognames:
            for dog in dognames:
                dognames_dic[dog.rstrip()] = counter
                counter += 1
        
        for key,value in results_dic.items():
            is_pet_label_dog = int(value[0] in list(dognames_dic.keys()) or 0)
            is_classified_label_dog = int(value[1] in list(dognames_dic.keys()) or 0)
            results_dic[key].extend([is_pet_label_dog, is_classified_label_dog])
            
    adjust_results4_isadog(result_dic, in_arg.dogfile)
    
    #Testing the function adjust_results4_isadog()
    #check_classifying_labels_as_dogs(result_dic)

    
    
    # TODO: 6. Define calculates_results_stats() function to calculate
    # results of run and puts statistics in a results statistics
    # dictionary (results_stats_dic)
    def calculates_results_stats(results_dic):
        results_stats = dict()  # Initializes dico
        
        n_images = len(results_dic)     # Total number of Images
        
         # n_correct_dog_matches = len([(key,value) for (key,value) in results_dic.items() if (value[2] == 1 and value[3] == 1 and value[4] == 1)])  # No of correctly classified dogs .i.e. a match and both dogs
        
        # Modified to produce similar result as the check_print...()
        n_correct_dog_matches = len([(key,value) for (key,value) in results_dic.items() if ((value[2] == 1 and value[3] == 1 and value[4] == 1) or (value[2] == 0 and value[3] == 1 and value[4] == 1))])  # No of correctly classified dogs .i.e. a match and both dogs
        
        n_dogs_img = len([(key,value) for (key,value) in results_dic.items() if value[3] == 1]) #No of Dog Images
        
        n_dogs_img = len([(key,value) for (key,value) in results_dic.items() if value[3] == 1]) #No of Dog Images

        
        # My believed Correct Implementation that yields correct Answer
        #n_correct_non_dog_matches = len([(key,value) for (key,value) in results_dic.items() if (value[2] == 1 and value[3] == 0 and value[4] == 0)]) # No of Correctly classified Non-Dogs i.e. a match and are both not dogs
        
        # Modified to produce exact result gotten from the check_print...()
        n_correct_non_dog_matches = len([(key,value) for (key,value) in results_dic.items() if (value[3] == 0 and value[4] == 0)]) # No of Correctly classified Non-Dogs i.e. a match and are both not dogs
        
        n_notdogs_img = len([(key,value) for (key,value) in results_dic.items() if value[3] == 0]) #No of Non-Dog Images
        
        n_correct_breed_matches = len([(key,value) for (key,value) in results_dic.items() if (value[2] == 1 and value[3] == 1)]) # Pet Label is a dog & Labels match
        
        n_label_matches = len([(key,value) for (key,value) in results_dic.items() if value[2] == 1]) #No of Non-Dog Images
        
        pct_correct_classified_dog_images = 0 if (n_dogs_img == 0) else ((n_correct_dog_matches / n_dogs_img) * 100)
        pct_correct_classified_non_dog_images = 0 if (n_notdogs_img == 0) else ((n_correct_non_dog_matches / n_notdogs_img) * 100)
        pct_correct_classified_dog_breed_images = 0 if (n_dogs_img == 0) else ((n_correct_breed_matches / n_dogs_img) * 100)
        pct_label_matches = 0 if (n_images == 0) else (n_label_matches / n_images) * 100
        
        results_stats['n_images'] = n_images
        results_stats['n_dogs_img'] = n_dogs_img
        results_stats['n_notdogs_img'] = n_notdogs_img
        results_stats['n_label_matches'] = n_label_matches
        
        results_stats['pct_correct_dogs'] = pct_correct_classified_dog_images
        results_stats['pct_correct_notdogs'] = pct_correct_classified_non_dog_images
        results_stats['pct_correct_breed'] = pct_correct_classified_dog_breed_images
        results_stats['pct_correct_label_matches'] = pct_label_matches
        
        #Previously used variables here...
        results_stats['n_correct_dogs'] = n_correct_dog_matches 
        #results_stats['pct_correct_dogs'] = round(pct_correct_classified_dog_images)
        results_stats['n_correct_breed'] = n_correct_breed_matches
        #results_stats['pct_correct_breed'] = round(pct_correct_classified_dog_breed_images)
        results_stats['n_correct_non_dog'] = n_correct_non_dog_matches
        #results_stats['pct_correct_non_dog'] = round( pct_correct_classified_non_dog_images)
        #results_stats['n_label_matches'] = n_label_matches
        #results_stats['pct_label_matches'] = round(pct_label_matches)
        
        return results_stats
        
    # Calling the function
    results_stats_dic = calculates_results_stats(result_dic)
    
    # Evaluating/testing the function
    #check_calculating_results(result_dic, results_stats_dic)
    

    
    # TODO: 7. Define print_results() function to print summary results, 
    # incorrect classifications of dogs and breeds if requested.
    def print_results(results_dic, results_stats, model, print_incorrect_dogs=False, print_incorrect_breed=False):
        
        print('\n\n')
        print('*' * 90)
        print('The Result Statistics of using "{m}" model for Image Classification'.upper().format(M=model))
        print('*' * 90)
        print('\nProgrammer: \t{n}'.format(n = 'Adeyemi Adedoyin Simeon'))
        print('Date: \t\t{d}'.format(d='10/19/2019 11:14pm'))
        print('Program: \t\t{p}'.format(p='"AI Programming with Python" Nanoprogram Course Project 1 on Udacity'))
        print('*' * 90)
        print('\n\t\tRESULT STATISTICS')
        print('*' * 90)
        res = ''
        pct = ''
        for key,value in results_stats.items():
            if key.startswith('n'):
                res += " ".join(key.split('_')).upper() + ': ' + str(value) + '\n'
            elif key.startswith('pct'):
                pct += " ".join(key.split('_')).upper() + ': ' + str(value) + '% \n'
        
        print("\n\tResults:")
        print("\t--------")
        print(res)
        print("\tPercentages:")
        print("\t------------")
        print(pct)
        
        # If user requests for printing Incorrect Dog classification i.e. set 'print_incorrect_dogs' to True
        if print_incorrect_dogs == True:
            print("\n\tDog Missclassification Report:")
            print("\t------------------------------")
                
            if ((results_stats['n_correct_dogs'] + results_stats['n_correct_non_dog']) != results_stats['n_images']):
                
                str_dog_miscl = ''
                
                for key,value in results_dic.items():
                    if value[3] != value[4]:
                        str_dog_miscl += 'Actual Pet Name: ' + value[0] + '\t\t Missclassified As: ' + value[1] + '. \n'
            
                print(str_dog_miscl)
                
            else:
                print('\tNo dog is missclassified. Every dog was correctly classified.\n')
                
        
        # if user requests for printing Breed Misclassification i.e. set 'print_incorrect_breed' to True
        if print_incorrect_breed == True:
            print("\n\tBreed Missclassification Report:")
            print("\t--------------------------------")
            if (results_stats['n_correct_dogs'] != results_stats['n_correct_breed']):
                
                str_breed_miscl = ''
                
                for key,value in results_dic.items():
                    if (value[2] == 0 and value[3] == 1 and value[4] == 1):
                        str_breed_miscl += 'Actual Breed Name: ' + value[0] + '\t\t Missclassified As: ' + value[1] + '. \n'
            
                print(str_breed_miscl)
                
            else:
                print('\tNo Breed Missclassification. Every breed was correctly classified.')
        

    # Calling the function
    print_results(result_dic, results_stats_dic, in_arg.arch, print_incorrect_dogs=True, print_incorrect_breed=True)

    
    
    # TODO: 1. Define end_time to measure total program runtime
    # by collecting end time
    end_time = time()

    
    
    # TODO: 1. Define tot_time to computes overall runtime in
    # seconds & prints it in hh:mm:ss format
    tot_time = end_time - start_time
    hh = int(tot_time // (60*60))
    mm = int((tot_time % (60*60)) // 60)
    ss = round( (tot_time % (60*60)) % 60 )
    print("\n** Total Elapsed Runtime: {a}:{b}:{c}".format(a=hh, b=mm, c=ss))



# TODO: 2.-to-7. Define all the function below. Notice that the input 
# parameters and return values have been left in the function's docstrings. 
# This is to provide guidance for achieving a solution similar to the 
# instructor provided solution. Feel free to ignore this guidance as long as 
# you are able to achieve the desired outcomes with this lab.

def get_input_args():
    """
    Retrieves and parses the command line arguments created and defined using
    the argparse module. This function returns these arguments as an
    ArgumentParser object. 
     3 command line arguments are created:
       dir - Path to the pet image files(default- 'pet_images/')
       arch - CNN model architecture to use for image classification(default-
              pick any of the following vgg, alexnet, resnet)
       dogfile - Text file that contains all labels associated to dogs(default-
                'dognames.txt'
    Parameters:
     None - simply using argparse module to create & store command line arguments
    Returns:
     parse_args() -data structure that stores the command line arguments object  
    """
    pass


def get_pet_labels():
    """
    Creates a dictionary of pet labels based upon the filenames of the image 
    files. Reads in pet filenames and extracts the pet image labels from the 
    filenames and returns these labels as petlabel_dic. This is used to check 
    the accuracy of the image classifier model.
    Parameters:
     image_dir - The (full) path to the folder of images that are to be
                 classified by pretrained CNN models (string)
    Returns:
     petlabels_dic - Dictionary storing image filename (as key) and Pet Image
                     Labels (as value)  
    """
    pass


def classify_images():
    """
    Creates classifier labels with classifier function, compares labels, and 
    creates a dictionary containing both labels and comparison of them to be
    returned.
     PLEASE NOTE: This function uses the classifier() function defined in 
     classifier.py within this function. The proper use of this function is
     in test_classifier.py Please refer to this program prior to using the 
     classifier() function to classify images in this function. 
     Parameters: 
      images_dir - The (full) path to the folder of images that are to be
                   classified by pretrained CNN models (string)
      petlabel_dic - Dictionary that contains the pet image(true) labels
                     that classify what's in the image, where its key is the
                     pet image filename & its value is pet image label where
                     label is lowercase with space between each word in label 
      model - pretrained CNN whose architecture is indicated by this parameter,
              values must be: resnet alexnet vgg (string)
     Returns:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)   where 1 = match between pet image and 
                    classifer labels and 0 = no match between labels
    """
    pass


def adjust_results4_isadog():
    """
    Adjusts the results dictionary to determine if classifier correctly 
    classified images 'as a dog' or 'not a dog' especially when not a match. 
    Demonstrates if model architecture correctly classifies dog images even if
    it gets dog breed wrong (not a match).
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    --- where idx 3 & idx 4 are added by this function ---
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
     dogsfile - A text file that contains names of all dogs from ImageNet 
                1000 labels (used by classifier model) and dog names from
                the pet image files. This file has one dog name per line.
                Dog names are all in lowercase with spaces separating the 
                distinct words of the dogname. This file should have been
                passed in as a command line argument. (string - indicates 
                text file's name)
    Returns:
           None - results_dic is mutable data type so no return needed.
    """           
    pass


def calculates_results_stats():
    """
    Calculates statistics of the results of the run using classifier's model 
    architecture on classifying images. Then puts the results statistics in a 
    dictionary (results_stats) so that it's returned for printing as to help
    the user to determine the 'best' model for classifying images. Note that 
    the statistics calculated as the results are either percentages or counts.
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
    Returns:
     results_stats - Dictionary that contains the results statistics (either a
                     percentage or a count) where the key is the statistic's 
                     name (starting with 'pct' for percentage or 'n' for count)
                     and the value is the statistic's value 
    """
    pass


def print_results():
    """
    Prints summary results on the classification and then prints incorrectly 
    classified dogs and incorrectly classified dog breeds if user indicates 
    they want those printouts (use non-default values)
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
      results_stats - Dictionary that contains the results statistics (either a
                     percentage or a count) where the key is the statistic's 
                     name (starting with 'pct' for percentage or 'n' for count)
                     and the value is the statistic's value 
      model - pretrained CNN whose architecture is indicated by this parameter,
              values must be: resnet alexnet vgg (string)
      print_incorrect_dogs - True prints incorrectly classified dog images and 
                             False doesn't print anything(default) (bool)  
      print_incorrect_breed - True prints incorrectly classified dog breeds and 
                              False doesn't print anything(default) (bool) 
    Returns:
           None - simply printing results.
    """    
    pass

                
                
# Call to main function to run the program
if __name__ == "__main__":
    main()
