from collections import deque

#Σώμα συναρτήσης χρονοπρογραμματισμού με fcfs

def simulate_fcfs(ls):
    
    #Αρχικοποίηση μεταβλητών
    
    file= ""
    total_seconds=0 
    total_wait=0
    
    #Για κάθε διεργασία στην λίστα 
    
    for (name,duration) in ls:
       
        #Αρχικοποιήση μετρητή
       
        counter=0
        wait_time = total_seconds
        #Όσο ο μετρητής είναι μικρότερος της συνολικής διάρκειας της διεργασίας
       
        while counter<int(duration):
            file += f"t={total_seconds}:{name}\n"   #Προσθήκη σειρών στη βοηθητική μεταβλητή για την δημιουργία του schedule_fcfs.txt
            total_seconds+=1                        #Αύξησε τα συνολικά δευτερόλεπτα κατα 1
            counter+=1                              #Αύξησε τον μετρητή κατά 1
        
        #Προσθήκη συνολικής διάρκειας της διεργασίας στο συνολικό χρόνο αναμονής
        total_wait+=wait_time
    
    avg=total_wait/len(ls)
    print(f'Ο συνολικός χρόνος ολοκλήρωσης των διεργασιών με FCFS είναι: {total_seconds-1} δευτερόλεπτα\nΟ μέσος χρόνος αναμονής των διεργασιών ήταν: {avg:.2f} δευτερόλεπτα')
    
    return file

#Σώμα συναρτήσης χρονοπρογραμματισμού με rr

def schedule_rr(ls):
    
    #Αρχικοποίηση μεταβλητών και δημιουργία deque
    
    file=""
    total_seconds=0
    total_wait=0
    q =deque()
    finish={}
    
    # Προσθήκη των στοιχείων της λίστας στην deque 

    for (name,duration) in ls:
        q.append((name,int(duration)))

    # Όσο υπάρχουν εκτελέσιμες διεργασίες

    while q:
        
        #Αρχικοποίηση μεταβλητών
        
        counter=0
        quantum_counter=0
        
        # Αφαίρεση πρώτης διεργασίας απο την deque και εκτέλεση της
        
        current_processor=q.popleft()
        name=current_processor[0]
        duration=current_processor[1]

        #Όσο ο μετρητής είναι μικρότερος της υπολοιπόμενης διάρκειας της διεργασίας

        while counter < duration:
            file += f"t={total_seconds}:{name}\n"   #Βοηθητική μεταβλητή για την δημιουργία του schedule_rr.txt
            quantum_counter+=1                      #Αύξησε το μετρητή του quantum κατά 1
            total_seconds+=1                        #Αύξησε τα συνολικά δευτερόλεπτα κατά 1
            counter+=1                              #Αύξησε τον μετρητή κατά 1
            
            # Έλεγχος για το αν το quantum ειναι 2 και ταυτόχρονα αν η διεργασία δεν έχει ολοκληρωθεί ωστέ να ξανατοποθετηθεί στην deque
            
            if quantum_counter == 2  and counter < duration: 
                q.append((name,duration-2))
                break
            
            # Όταν ολοκληρωθεί η διεργασία αποθήκευσε την χρονική στιγμή που συνέβη
            
            if counter == duration:
                finish[name]=total_seconds

    #Υπολογισμός του συνολικόυ χρόνου αναμονής όλων των διεργασιών
    
    for (name,duration) in ls:
            wait_time=int(finish[name])-int(duration)  
            total_wait+=wait_time

    avg=total_wait/len(ls)  

    print(f'Ο συνολικός χρόνος ολοκλήρωσης των διεργασιών με RR είναι: {total_seconds-1} δευτερόλεπτα\nΟ μέσος χρόνος αναμονής των διεργασιών ήταν: {avg:.2f} δευτερόλεπτα')
    return file 


#------------------------------------------------------------------------

# Εκτέλεση της κατάλληλης μεθόδου και αποθήκευση των αποτελεσμάτων σε αρχείο schedule_xx.txt

def run(ls,method):
    
    
    if method=='FCFS':
        output_txt = simulate_fcfs(tlist)
    else:
        output_txt = schedule_rr(tlist)

            
    open("schedule_fcfs.txt",'w',encoding="utf-8").write(output_txt) if method=='FCFS' \
        else open("schedule_rr.txt",'w',encoding='utf-8').write(output_txt)
    
#------------------------------------------------------------------------

file_path=input("Δώσε το όνομα ή την διαδρομή του αρχείου UTF-8: ")

# Απαραίτητος έλεγχος για το άνοιγμα του αρχείου και τοποθέτηση των στοιχειών του αρχείου σε κατάλληλες δομές 

try:
    with open(file_path, "r",encoding="utf-8") as f:
        tlist=[]
        for line in f:
            
            linestrip=line.strip()

            if not linestrip or linestrip.startswith("#"):
                continue
            
            linesplit=linestrip.split()
            tuplem=(linesplit[0],linesplit[1])
            tlist.append(tuplem)
        
        run(tlist,'FCFS') 
        run(tlist,'RR')
except FileNotFoundError:
    print('Το αρχείο δεν βρέθηκε')
except UnicodeDecodeError:
    print('Το αρχείο δεν είναι σε UTF-8 κωδικοποίηση.')