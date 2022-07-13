from django.core.management.base import BaseCommand, CommandError
from movies.models import Film, Decade

class Command(BaseCommand):
    help = 'Sets up the movies database.'

    def handle(self, *args, **options):
        Decade.objects.get_or_create(
            decade='1900',
            title='The Silent Era (1878-1929)',
            description=
            '''
            Imagine its the year 1878 for a second. You've seen some print photographs before but never any that were moving. All of a sudden you experience a picture that does appear to be moving. Its a picture of a horse running endlessly to the right, but yet remains within the frame. You are shocked and amazed at what you are seeing. Not only does it seem like magic, but you are excited to see other pictures of things you recognize moving in this new-found plane. This is how people felt upon seeing the first "films."

            During the silent era of film, audiences went to films for their spectacle rather than their narratives or writing. It was a period that could be considered a "Cinema of Attractions." People were shocked by the moving images on the screen. Each film generally lasted under a minute long and was usually just a single scene. Common scenes were of everyday life, public events, sporting events or slapstick gags. There was no real cinematic technique during this period so to engage audiences many films were hand painted to add color. Some theatres and films would go as far as to use orchestras and performers to score and explain what was happening on the screen. In order to bypass the need for a performer, however, films eventually adopted the use of intertitle cards to provide dialogue and better context for the events unfolding.

            The entire film industry was built around the novelty of moving pictures. Films were a relatively cheap way of providing entertainment to people all over the world. As demand for more films grew, studios started focusing on mass production rather than whether each film was good or not. Producers were hired to watch over the productions of films and made sure development quotas were met. Eventually people demanded a higher quality, and so by the 1920s better narratives became more commonplace.

            Fun Fact: Nickelodeons were theaters that charged a Nickle to get in. They were wildly successful.

            Personal Favorites of the Era: Sherlock Jr. and Sunrise.
            ''',
        )
        Decade.objects.get_or_create(
            decade='1930',
            title='The Golden Age of Hollywood (1930-1945)',
            description=
            '''
            A period of escapism where people chose to watch films during The Great Depression because they were cheap and accessible entertainment. Popular genres were Screwball Comedies, Westerns, and Musicals. Studios aimed to push boundaries and have the most exciting films on the block. This became difficult when The Hays Code was established in 1934 by the American government putting certain censorship rules on studios, such as no pointed swearing, lustful kissing and you had to be delicate with theft and robbery. Murder was still fine of course, and boy is there a lot of it in these films. The Hays Code forced Studios to be creative when trying to push the boundary, having to weave around various rules to tell their stories and still shock audiences. Unfortunately, Studios took another hit in the late '40s when the American government declared that Studios were in violation of antitrust Laws (having a monopoly on film entertainment) and were forced to sell their theater holdings. Now they could only focus on production and distribution of films, not Theatre showings.

            Despite these setbacks however, Studios still had near unlimited freedom to produce artistic, commercially successful films that still stand the test of time as some of the best ever made. During this Era, Studios refined the style of American films into the bedrock of what it is today. The American films we see today still have the structure and DNA of the films produced during this Era. Also a big thanks to the introduction of Color in 1939, upping the ante for films and better allowing audiences to engage with the pictures they were watching.

            Fun Fact: As people moved out of urban centers and into the suburbs, studios switched to purchasing drive in movie theaters in order to distribute their films.

            Personal Favorites of the Decade: Mr. Smith Goes to Washington, City Lights, King Kong,and Angels with Dirty Faces.
            ''',
        )
        Decade.objects.get_or_create(
            decade='1940',
            title="The End of Hollywood's Golden Age (1930-1945) and Rise of The Foreign Wave (1945-1970)",
            description=
            '''
            Due to audience's changing film tastes post-World War II, the 1940s spelled the death of Hollywood's Golden Age and the advent of a new Foreign Wave of cinema. Audiences all over the world were beginning to tire of the artificial tone of American Hollywood films, which began to feel self-important and inauthentic. By the mid 1940s, audiences were ready for something new. There began a new attention to cinema as art and national expression and this began with Roberto Rossellini's Rome, Open City (1945) and Italian Neo-Realism.

            Neo-realism was raw and felt real, in part due to their shoe-string budgets compared to the U.S. These films attempted to accurately project the authentic suffering felt by real people following the war. Films were shot on location, endings were ambiguous, and just generally looked rougher than the crisp cleanliness that American Hollywood films had. All of these elements of Italian New-Realism attracted jaded film audiences post World War II.

            To clarify, of course 1945 is not the death of Hollywood or its films. During these decades Hollywood would produce some classics that we largely still hear about today. Hitchcock, Welles, Kubrick, and Ford were all in their prime during this time. However, the dominance of Hollywood's cultural hold over films produced was severely shaken and, while they still produced some marvellous pieces of cinema, it became mostly international directors that were leading the way in the artistic cutting edge of what films had to offer.

            Fun Fact: Huddling around the radio was a key source of quality family time and entertainment throughout the decade, before television completely took over everything in the ’50s. People listened in for war updates, quiz shows, soap operas, sports broadcasts, and more.

            Favorites of the Decade: The Philadelphia Story (1940), Mrs. Miniver (1942).
            ''',
        )
        Decade.objects.get_or_create(
            decade='1950',
            title="The Rise of Japanese Cinema (1950s)",
            description=
            '''
            While many American classics were produced during this decade, World cinema as a whole, and particularly Japanese cinema, was going gangbusters. This is no more apparent than the rise of legendary Japanese filmmakers Akira Kurosawa (Seven Samurai) and Yasujiro Ozu (Tokyo Story) who became international superstars.

            Post-World War Two Japan was scarred both physically and psychologically by the devestation left in the wake of the Atomic bombs dropped on Hiroshima and Nagasaki. The effects of this devestation can be glimpsed in their film's of the decade. Godzilla (1954) was a metaphor for nuclear holocaust. Kurosawa's breakout film, Rashomon, emphasized that there are always conflicting sides to any story. Ozu's Tokyo Story (1953) touched on the break up and Westernization of the traditional Japanese family after World War II.

            Back in America, cinemas had entered into a war with the increasingly popular Television. To combat this threat, theatres promoted Cinemascope and other ultra-widescreen technologies to draw butts out of homes and put them in auditoriums. Massive scale movie epics like The Ten Commandments (1956) and Ben-Hur (1959) benefited greatly from these campaigns.

            The most popular American genre at this time was Sci-fi, on account of the newly introduced Atomic Bomb. Popcorn flicks like The Day the Earth Stood Still (1951) and The Thing from Another World (1951) were the best that American sci-fi had to offer during this period.

            Also during the decade, Alfred Hitchcock was at the height of his powers with Rear Window, Vertigo, and North by Northwest. John Ford and John Wayne revitalized the Western genre in 1956 with The Searchers. And Bengali Indian director Satyajit Ray released his critically acclaimed Apu Trilogy (1955–1959).

            Fun Fact: The special effects skills Japanese filmmakers learned shooting war propaganda films during WWII were paramount in producing action films like Godzilla.

            Favorites of the Decade:
            ''',
        )
        Decade.objects.get_or_create(
            decade='1960',
            title="The French New Wave (1960s) & The Rise of The Film School Generation (1967 - 1985)",
            description=
            '''

            ''',
        )
        Decade.objects.get_or_create(
            decade='1970',
            title="New Hollywood: The Film School Generation (1970-1985)",
            description=
            '''

            ''',
        )
        Decade.objects.get_or_create(
            decade='1980',
            title="New Hollywood and the Rise of Independent Cinema (1985-1995)",
            description=
            '''

            ''',
        )
        Decade.objects.get_or_create(
            decade='1990',
            title="Contemporary Cinema (1995 - Today)",
            description=
            '''

            ''',
        )
        Decade.objects.get_or_create(
            decade='2000',
            title="Contemporary Cinema (1995 - Today)",
            description=
            '''

            ''',
        )
        Decade.objects.get_or_create(
            decade='2010',
            title="Contemporary Cinema (1995 - Today)",
            description=
            '''

            ''',
        )
        Decade.objects.get_or_create(
            decade='2020',
            title="Contemporary Cinema (1995 - Today)",
            description=
            '''

            ''',
        )

        Film.objects.get_or_create(
            title='Sherlock Jr.',
            year="1924",
            rating='',
            description=
            '''
                A film projectionist longs to be a detective, and puts his meagre skills to work when 
                he is framed by a rival for stealing his girlfriend's father's pocketwatch.
            ''',
            director='Buster Keaton',
            writer='Jean C. Havez, Joseph A. Mitchell',
            cast='Buster Keaton, Kathryn McGuire, Joe Keaton',
            studio='United States of America',
            country='Metro Pictures (Forerunner of MGM)',
            reviews='''
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
            image='/Users/arbelaezch/code/arbelaezch.ca/website/media/movie-posters/sherlock jr.jpeg',
            decade_fk=Decade.objects.get(decade='1900'),
        )

        # Film.objects.get_or_create(
        #     title='',
        #     year="",
        #     rating='',
        #     description=
        #     '''

        #     ''',
        #     director='',
        #     writer='',
        #     cast='',
        #     studio='',
        #     country='',
        #     reviews='',
        #     image='',
        #     decade_fk='',
        # )


        self.stdout.write('Movie database setup successful!')
