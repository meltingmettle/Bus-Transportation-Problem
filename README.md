# CS170 Final Project: Bus Transportation Problem

# Problem 
Design an approximation algorithm for a maximally connected K-clusters problem with several parameter constraints.
Given a graph G, group all vertices into subgraphs of size b while maximizing the number of edges within each list, and keeping another set of parameter vertex groups separate.  

    You are a tired, overworked teacher who has spent the last week organizing
    a field trip for your entire middle school. The night before the trip, you
    realize you forgot to plan the most important part – transportation! Fortunately,
    your school has access to a large fleet of buses. Being the caring teacher
    you are, you’d like to ensure that students can still end up on the same bus
    as their friends. After some investigative work on social media, you’ve managed
    to figure out exactly who is friends with who at your school and begin to
    assign students to buses with the intent of breaking up as few friendships as
    possible. You’ve only just begun when you receive a frantic email from one of
    the chaperones for the trip. The kids this year are particularly rowdy, and the
    chaperones have given you a list of groups of students who get too rowdy when
    they are all together. If any of these groups are seated assigned to the same
    bus, they will all have to be removed from the bus and sent home. Can you
    plan transportation while keeping both the students and the chaperones happy?

http://emmettling.me/CS_170_FA18_Project_Spec.pdf
(Same link as in the repo description)

# Approach
See the Project Final Report!

# Result
Our latest submission scored in the highest tier (top 20%) of our class of 800+ other students with a score of around 0.46, meaning our algorithm maintained ~46% of total edge relationships. (The closest approximation was around 53%, with the mean score around 37%)(Ratio calculated by intact_friendships/G_total_edges.  Obviously, as we were approximating an NP-hard problem with a large sample student-generated inputs, no optimal solution was available to measure by.)  

# Additional Notes for Future Reference
In retrospect, it would have been wise to create class representations of each variable/parameter.  Our team spent the majority of our time brainstorming the pros and cons of different approaches and we lept into implementation after choosing our five best approaches.  This ended up costing time later, when we began combining code and connecting the various handlers.  In addition, implementing class representations of each attribute would have been doable within the first day of reading the project since it only requires a basic understanding of the prompt and it could have even inspired us with new ideas.

Additionally, it would have been wise to establish AWS capability just in case, although we ended up not needing it due to the relatively short runtime of our algorithms.  

Well, all's well that ends well.

# Thank Yous
Thanks to Professor Rao, Professor Chiesa, and Sam Zhou, our TA who provided guidance and invaluable mentoring throughout the course as well as through the entire project.  Your passion for algorithms shone through your teaching and inspired us through the semester!

Additional thanks to my long-time friends and partners Maryam and Aidan. 
I really appreciate your hard work, dedication to excellence, calm under pressure, teamwork, and great personality which made you both a pleasure to work with! I hope we have the chance to collaborate more in the future!

--Emmett, Maryam, and Aidan
