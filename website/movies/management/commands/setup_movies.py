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
            image=''
        )

        self.stdout.write('Movie database setup successful!')
