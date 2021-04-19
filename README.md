Spacedbooks
==========
This is a command line tool that provides convenient way to manage "spaced repetition" of books to faciliate  
effective long-term learning.  

Workflow:
--------
   1. You've read new book 3 days ago.  
   2. Add this book into db: `spacedbooks add-book "The Shallows" "Nicholas Carr" --isbn=978-0393357820 -0`.  
   3. Check intervals in config and set them to your prefered spaced repetition schedule. Since most spaced  
       repetition research is limited to short-term retrieval, I've found only single truly relevant research  
       paper and adopted its recommendations in the default config intervals.  
       (Spacing effects in learning: A temporal ridgeline of optimal retention - https://escholarship.org/uc/item/0kp5q19x).  
   4. Use `spacedbooks.py` without arguments to generate list of books that should be reviewed or use  
       cron, launchd etc. to run `spacedbooks.py send-mail` periodically to receive notifications by email.  
    
        ```
        ===================
        ‖ BOOKS TO REVIEW ‖
        ===================
        [4] "The Coddling of the American Mind: How Good Intent..." by Jonathan Haidt
        [3] "Digital Minimalism: Choosing a Focused Life in a N..." by Cal Newport
        [2] "Understanding How We Learn: A Visual Guide" by Yana Weinstein, Megan Sumeracki
        [1] "The Warship" by Neal Asher
        [5] "The Shallows" by Nicholas Carr
        ```
   5. Run `spacedbooks.py add-review ...` to log that you have reviewed the book.
