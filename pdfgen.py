from fpdf import FPDF



class PDF(FPDF):

    def header(self):

        title = 'My Home Insurance Document'
        self.set_font('helvetica','B',15)
        #Calculate the width of title and position
        title_w = self.get_string_width(title) + 6
        doc_w = self.w
        self.set_x((doc_w-title_w)/2)
        #colors of frame, background, and text 
        self.set_draw_color(0,80,180) #border = blue
        self.set_fill_color(230,230,0) #background - yellow
        self.set_text_color(220,50,50) # Text = red
        #Thickness of Frame (border)
        self.set_line_width(1)
        #Title
        self.cell(title_w,10,title,border=1,ln=1,align='C',fill=1)
        #Line Break
        self.ln(10)

    def footer(self):
        # Set Position of the footer
        self.set_y(-15)
        #Self font
        self.set_font('helvetica','I',8)
        #Set fornt colory grey
        self.set_text_color(169,169,169)
        #Page Number
        self.cell(0,10,f'Page{self.page_no()}',align='C')

    def chapter_title(self,ch_num,ch_title):
        #set font
        self.set_font('helvetica','',12)
        # background color
        self.set_fill_color(200,220,255)
        #Chapter Title
        chapter_title = f'Chapter {ch_num} : {ch_title}'
        self.cell(0,5,ch_title,ln=1,fill=1)
        #line break
        self.ln()

    #Chapter Content                
    def chapter_body(self,name):
        #read text file
        with open(name,'rb') as fh:
            txt = fh.read().decode('latin-1')
        #set font
        self.set_font('times','',12)
        # insert text
        self.multi_cell(0,5,txt)
        #line break
        self.ln()
        #end each chapter
        self.set_font('times','I',12)
        self.cell(0,5,'END OF CHAPTER')



    def print_chapter(self,ch_num,ch_title,name):
        self.add_page()
        self.chapter_title(ch_num,ch_title)
        self.chapter_body(name)

# #create a PDF object
# pdf = PDF('P','mm','Letter')

# #Set auto page break
# pdf.set_auto_page_break(auto = True,margin = 15)



# pdf.print_chapter(1,'What is Covered','chp1.txt')
# pdf.print_chapter(2,'What is not Covered','chp2.txt')


# pdf.output('pdf_3.pdf')


  


         

         
