from django.core.management.base import BaseCommand, CommandError
from movies.models import Film, Decade

class Command(BaseCommand):
    help = 'Sets up the movies database.'

    def handle(self, *args, **options):

        Film.objects.get_or_create(
            title="The Great Train Robbery ",
            year="1903",
            rating="",
            description="A group of bandits stage a brazen train hold-up, only to find a determined posse hot on their heels.",
            director="Edwin S. Porter",
            writer="Edwin S. Porter",
            cast="Gilbert M. 'Broncho Billy' Anderson, A.C. Abadie, George Barnes",
            studio="Edison Manufacturing Company",
            country="America",
            review='''A massive success that served as one of the vehicles that would launch film as a medium into mass popularity. From the very beginning, people proved they love their Wild West violence. Cinematography wise, there is some incredible stuff in here! There is a Panning Shot in here! For those that may not know, a Panning Shot is a camera movement where you pan the camera from right to left. Better than just this single shot however, Director Edwin S. Porter uses a panning shot to reveal to the audience that there have been some horses off screen that the robbers can use to escape. This is an enormous leap in filmmaking as Porter is using the camera to tell the story. Imagine a film where the camera is static and all the information is readily available to the viewer. Now imagine a film where information is slowly revealed piece by piece keeping the audience on their toes. This second film is infinitely more interesting to watch.
            
                        Another incredible cinematographic technique pioneered in this picture is Parallel Action. Parallel action is when a film does a cross cut from two events that are occurring simultaneously. Once again this is a technique that allows for greater story telling freedom. 
                        
                        
                        And of course the most visible narrative technique, the star of the show, is the fourth wall break at the end where a rogue cowboy appears and shoots at the audience. People of the time were unfamiliar with moving pictures and how exactly they operated and so you can imagine all the chaos that would ensue from unsuspecting audience members ducking out of the way of the perceived incoming shots.
                        ''',
            image="train robbery.jpeg",
            decade_fk=Decade.objects.get(decade="1900"),
        ),
        Film.objects.get_or_create(
            title="Metropolis ",
            year="1927",
            rating="",
            description="In a futuristic city sharply divided between the working class and the city planners,the son of the city's mastermind falls in love with a working class prophet who predicts thecoming of a savior to mediate their differences.",
            director="Fritz Lang",
            writer="Thea von Harbou",
            cast="Brigitte Helm, Alfred Abel, Gustav Fröhlich",
            studio="UFA",
            country="Germany",
            review='''
                "The mediator between the head and the hands must be the heart."
              
                One of the early epic science fiction pictures to wow audiences with it's pioneering special effects. 
                Techniques such as using miniature models of the city, using a camera on a swing, a giant robot costume worn by
                an actor, and finally the Shufftan Process, which uses mirrors to create the illusion that actors
                 are occupying miniature sets. However, even with these novel effects for the time and its enormous budget, Metropolis
                was still released to mixed reception from critics and audiences. People heralded it as beautiful and visually powerful
                 but lacking in story, with some going as far as to call the story trite and silly. Of course nowadays people 
                claim it is one of the best science fiction pictures of the age, and for good reason.

                The film was born from its director, Fritz Lang seeing the skyscrapers in New York City. Writer Thea von Harbou 
                also took inspiration for the plot from World War 1, as well as the culture of the Weimar Republic in Germany. With Metropolis 
                Harbou and Lang attempted to explore themes of industrialization and mass production and their effects on society as well as 
                how they impacted the war. 

                Personally, I found Metropolis to be far too long. At first I could appreciate the special effects, as well as the scale 
                of the project. But a two and a half hour runtime is just far too long to be propped up by effects. While it was an epic at one time, 
                its long since become obsolete in effects and message, with industrialization taking a back seat to Artificial Intelligence in our 
                "new age."
                ''',
            image="metropolis.jpeg",
            decade_fk=Decade.objects.get(decade="1900"),
        ),
        Film.objects.get_or_create(
            title="Birth of a Nation",
            year="1915",
            rating="",
            description="The Stoneman family finds its friendship with the Camerons affected by the Civil War,both fighting in opposite armies. The development of the war in their lives plays through toLincoln's assassination and the birth of the Ku Klux Klan.",
            director="D.W. Griffith",
            writer="Thomas Dixon Jr. (adapted from his novel: 'The Clansman: An Historical Romance of the Ku Klux Klan')",
            cast="Lillian Gish, Mae Marsh, Henry B. Walthall",
            studio="Epoch Producing Co.",
            country="America",
            review='''
                A true spectacle that is and alwasy has been marred in controversy. 
                Even at the time of release it was considered vile propaganda, sparking riots across the States. 
                It was a film that revitalized the Klan and anti-immigration movements.

                

                While, at the same time, it was and is a truly massive spectacle piece that 
                signalled the birth of long form narrative film in America and remained the highest grossing American film until
                Gone With the Wind in 1939. The film features close up shots along side massive military skirmishes and a sprawling story
                that covers the breadth of the entire country. It also rests at a comfortable three hours long, making it a highly
                irregular Epic for the time.

                
                

                Overall, it is a cinematic masterpiece that will forever remain the haunting shadow of every American made film going forward.
                ''',
            image="birth of a nation.jpeg",
            decade_fk=Decade.objects.get(decade="1900"),
        ),
        Film.objects.get_or_create(
            title="Sunrise: A Song of Two Humans ",
            year="1927",
            rating="",
            description="An allegorical tale about a man fighting the good and evil within him.Both sides are made flesh - one a sophisticated woman he is attracted to and the other his wife.",
            director="F.W. Murnau",
            writer="Carl Mayer, Hermann Sudermann",
            cast="George O'Brien, Janet Gaynor, Margaret Livingston",
            studio="Fox",
            country="America",
            review='''
                One of the first feature films with a synchronized musical score and sound effects soundtrack. 
                Also won Oscars for Unique and Artistic Picture (Best Picture before it was called BP), Actress, and Cinematography. 
                The cinematography Oscar is very much earned as it is an absolutely beautiful film that does a 
                wonderful job of conveying meaning as there are very few title cards, which is very much appreciated. 
                A couple of noteworthy moments are one where the main characters stand in the street with cars dashing by 
                them and another where the couple is on a boat in the middle of a storm. Cinematographically, this movie blows
                others out of the water!
               

                Unfortunately like so many other films during this era that I love, Sunrise was a box office flop. 
                Well at least it was critically received well because it is absolutely beautiful and a joy to watch.
            ''',
            image="sunrise.jpeg",
            decade_fk=Decade.objects.get(decade="1900"),
        ),
        Film.objects.get_or_create(
            title="Battleship Potemkin ",
            year="1925",
            rating="",
            description="In the midst of the Russian Revolution of 1905, the crew of the battleship Potemkinmutiny against the brutal, tyrannical regime of the vessel's officers.The resulting street demonstration in Odessa brings on a police massacre.",
            director="Sergei M. Eisenstein",
            writer="Nina Agadzhanova",
            cast="Aleksandr Antonov, Vladimir Barskiy, Grigoriy Aleksandrov",
            studio="Mosfilm",
            country="USSR",
            review='''
                A film that is considered today as one of the greatest films ever made and has had massive influence on cinema as a whole; 
                influencing prolific directors like Coppola and 
                De Palma. Battleship Potemkin is a massive movie, possibly more ambitious than Birth of a Nation? 
                It included Filming on water, huge numbers of extras, and a literal squadron of battleships. 
                There are some striking visuals (every film nerd loves the scene on the stairs), and boy of boy did 
                Sergei like his "montage." The montage being an editing technique pioneered in this film that was a 
                simple shot of someone, reverse shot to what theyre looking at, 
                and then a reaction shot back on number 1 again. This technique is supposed to provide more emotion.
                

                I definitely think the Russian editing style threw me off, I just couldn't get into its rhythm. I always 
                felt like the editing pace was either moving too quick or too slow. The step scene was shocking and visceral, 
                the last chapter was suspenseful, but I don't know it just didnt grip me. Also another thing is that I have no real 
                connection to the Russian revolution, so its hard for me to identify with these people. 
                
                This leads well into the fact this film is Revolutionary propaganda; and is hailed as one of the finest propaganda 
                films ever made. Joseph Goebbels took note of the film and used it as inspiration for his future work in Nazi propaganda.
                Though Sergei did do a good job of making the reason behind the Bolsheviks fury timeless. I think I'm just too 
                engrained in classical American editing to have gotten really into this one.
            ''',
            image="battleship potemkin.jpeg",
            decade_fk=Decade.objects.get(decade="1900"),
        ),
        Film.objects.get_or_create(
            title=" Un Chien Andalou ",
            year="1929",
            rating="",
            description="Luis Buñuel and Salvador Dalí present 21 minutes of bizarre, surreal imagery.",
            director="Luis Buñuel",
            writer="Salvador Dalí, Luis Buñuel",
            cast="Pierre Batcheff, Simone Mareuil, Luis Buñuel",
            studio="Les Grands Films Classiques",
            country="France",
            review='''
                "the Andalusian dog howls-someone has died!”
          
                What in the ever loving hell is this. I've seen some weird shit before but this is some weird shit. 
                The most concrete impression I get from this is of a surreal expressionist painting. 
                I get the sense you are not supposed to "understand" this film so much as you are supposed to experience it.

                The french are weird, man.

                Not so fun-fact: David Bowie showed the entire film to concert goers during his 1976 tour.
            ''',
            image="andalou.jpeg",
            decade_fk=Decade.objects.get(decade="1900"),
        ),
        Film.objects.get_or_create(
            title="A Trip to the Moon ",
            year="1902",
            rating="",
            description="A group of astronomers go on an expedition to the Moon.",
            director="Georges Méliès",
            writer="Georges Méliès",
            cast="Georges Méliès, Victor André, Bleuette Bernon",
            studio="Star Film Company",
            country="France",
            review='''
                The year is 1902 and audiences have grown from the "shock and awe" of seeing moving pictures of every-day life events, such as a train moving or a horse galloping. People wanted more. They wanted to be engaged by pictures now that their shock value had begun to wear off. Enter Georges Méliès, magician turned filmmaker who brought a narrative flair to films that transformed people from their regular lives and took them on a trip to the moon. 

                With film, "Méliès had found a way to perform actual magic with editing, to fool an audience and pull off illusions he'd never been able to do on stage."1

                Méliès pioneered several in-camera tricks, such as Double Exposure2, to trick audiences into believing the impossible, and once again shocking them. But he didn't stop there as, unlike other films of the time, Méliès brought in his extensive sets and props from his time as a stage magician to build upon his narratives until they gripped audiences and made them believe the story they were watching.
            
                Enter, A Trip to the Moon, as the first Science Fiction film ever made. A Trip to the Moon utilizes simple in-place shots with no close ups, such as had been done in George Albert Smith's short film, Grandma's Reading Glass from 1900. Yet despite the relatively basic cinematography, A Trip to the Moon was a massive international success and is considered a classic due to it being Méliès' biggest production to date. It was an unheard of for the time fifteen minutes long, and brought together all of the special effects tricks he had learned, as well as being his most ambitious story yet with beautiful sets and costumes to match. Audiences were hooked by his exciting space adventure as they had never seen a narrative picture like it before. With this single film Méliès' reinvented film production and narratives and inspired other filmmakers to follow in his artistic footsteps.
            
                1: https://www.youtube.com/watch?v=L8is28gAOTc&t=331s
                2: Double Exposure: A trick where you shoot footage twice over the same piece of film to make it look like two separate events are occurring at the same time.
            ''',
            image="a trip to the moon.jpeg",
            decade_fk=Decade.objects.get(decade="1900"),
        ),
        Film.objects.get_or_create(
            title="Sherlock Jr. ",
            year="1924",
            rating="",
            description="A film projectionist longs to be a detective, and puts his meagre skills to work whenhe is framed by a rival for stealing his girlfriend's father's pocketwatch.",
            director="Buster Keaton",
            writer="Jean C. Havez, Joseph A. Mitchell",
            cast="Buster Keaton, Kathryn McGuire, Joe Keaton",
            studio="Metro Pictures (Forerunner of MGM)",
            country="America",
            review='''
                An incredibly fun, accessible adventure that still holds audience engagement to this day! 
                Cinematography wise there are dream sequences, cutting between different scenes that take place 
                at the same time, moving shots, and a theatre scene that needs to be seen to be believed.
                I am super impressed. But this film goes beyond simple camera work, it instead rests on its 
                incredibly funny gags and stoic lead, Keaton. Near singlehandedly, Keaton brings you into 
                a story that actually grips and makes you feel for its participants. 
                

                Nearly all of the story is told through physical acting / visuals so there is not much reading involved. 
                Your time as a viewer is not wasted, but instead rewarded through clever visual cues that keep your eyes glued
                and your attention piqued. And not to mention the bike scene at the end oh my god! 
                I cannot believe some of the stunts. Truly impressive.

                The most heartbreaking thing about this entire picture is that it was not initially received well and was
                considered a box office failure. The only question I have is, HOW???
            ''',
            image="sherlock jr.jpeg",
            decade_fk=Decade.objects.get(decade="1900"),
        ),
        Film.objects.get_or_create(
            title="Steamboat Willie ",
            year="1928",
            rating="",
            description="Mickey Mouse, piloting a steamboat, delights his passenger, Minnie, by making musicalinstruments out of the menagerie on deck.",
            director="Ub Iwerks, Walt Disney",
            writer="Walt Disney",
            cast="Walt Disney",
            studio="Walt Disney Studios",
            country="America",
            review='''
                One of the first cartoon with fully ynchronized sound. Steamboat Willie became the most popular cartoon of its day
                not just from the introduction of the charasmatic and hilarious Mickey Mouse, but from the fully realized
                sound effects and sountrack to accompany the cartoon. This success stems from the fact that Walt Disney believed 
                sound was the future of cartoons and film alike. Thanks to Steamboat Willie, Walt Disney and Mickey Mouse 
                became household names that have remained at the heart of American cinema for nearly a hundred years.
                
                

                Aside from all that, its just a really fun cartoon.
            ''',
            image="steamboat willie.jpeg",
            decade_fk=Decade.objects.get(decade="1900"),
        ),
        Film.objects.get_or_create(
            title="The General ",
            year="1927",
            rating="",
            description="When Union spies steal an engineer's beloved locomotive, he pursues it single-handedly andstraight through enemy lines.",
            director="Clyde Bruckman, Buster Keaton",
            writer="Buster Keaton, Clyde Bruckman",
            cast="Buster Keaton, Marion Mack, Glen Cavender",
            studio="United Artists",
            country="America",
            review='''
                Made at the end of the silent era, Buster Keaton's magnum opus picture was a critical and 
                box office failure that lost Keaton his independence as a filmmaker. The General substitutes 
                some of the comedy from Sherlock Jr. for a much stronger dramatic narrative. This was to the dismay of the
                audience which was expecting to leave the theatre in stitches. 
                
                
                I too personally think it loses something in the trade off. The General is massive and 
                tense and shocking at times, but Sherlock was just clean and tight. I think The General can't stand on the drama 
                as successfully as Sherlock can stand on the comedy. Not to say that Keaton didn't make a highly engaging 
                drama that I think outshines almost anything else in the 20s. Its just comparing the succinct, rapid fire
                comedy of Sherlock Jr. to the far grander, slower comedy-narrative duo of The General, I'm gonna pick Sherlock 
                nine times outta ten. Either way I still really enjoyed it and still admire and respect Keaton's dedication to the gag. 
                Charlie Chaplin eat your heart out.
            ''',
            image="the general.jpg",
            decade_fk=Decade.objects.get(decade="1900"),
        ),
        Film.objects.get_or_create(
            title="The Gold Rush ",
            year="1925",
            rating="",
            description="A prospector goes to the Klondike in search of gold and finds it and more.",
            director="Charles Chaplin",
            writer="Charles Chaplin",
            cast="Charles Chaplin, Mack Swain, Tom Murray",
            studio="United Artists",
            country="America",
            review='''
                The fifth-highest-grossing silent film in cinema history and one of the high points of silent star, 
                Charlie Chaplin's career. I watched the 1942 version recut by Chaplin with his own narration and sharper editing
                and I gotta say, this is a pretty magnificent way to watch a silent film. With audio lol. 
                
                It is a really fun and heartfelt flick that is original (obviously) and fast paced. 
                It was really swell. Kind of like a quick treat of a film. You feel good after watching it. 
                Also some really nifty special effects like the house moving. Not as "spectacular" as Buster Keaton, 
                in my humble opinion, but of its own style that is still quite enjoyable.
            ''',
            image="gold rush.jpeg",
            decade_fk=Decade.objects.get(decade="1900"),
        ),
                        