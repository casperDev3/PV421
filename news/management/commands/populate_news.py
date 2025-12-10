from django.core.management.base import BaseCommand
from news.models import News
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Populates the database with mock news data'

    def handle(self, *args, **kwargs):
        titles = [
            "Senate Passes Historic Infrastructure Bill After Marathon Session",
            "Tech Giants Face New Regulations in European Union",
            "NASA's Latest Rover Sends Back Stunning Images from Mars",
            "Global Markets React to Fed's Interest Rate Decision",
            "New Study Shows Benefits of Mediterranean Diet on Heart Health",
            "Local Election Results Surprise Analysts Across the Country",
            "Breakthrough in Renewable Energy Storage Technology Announced",
            "Art Gallery Discovers Long-Lost Painting by Renaissance Master",
            "City Planning Commission Approves Controversial Skyscraper",
            "Weather Forecast Predicts Record Heatwave for Next Week"
        ]

        contents = [
            """In a landmark decision late last night, the Senate approved the sweeping infrastructure bill that has been the subject of intense debate for months. The legislation, which promises to revitalize the nation's aging roads, bridges, and public transit systems, passed with a bipartisan majority, signaling a rare moment of unity in a politically divided capital.

            Proponents of the bill argue it will create thousands of jobs and modernize the country's economic backbone. "This is a generational investment," said Senator Smith. However, critics remain concerned about the long-term fiscal impact.
            
            Key provisions include funding for high-speed rail, broadband internet expansion in rural areas, and significant upgrades to the power grid. The bill now heads to the House of Representatives, where a swift vote is expected.""",
            
            """The European Union has unveiled a new set of strict regulations aimed at curbing the power of major technology companies. The Digital Markets Act targets anti-competitive behavior and mandates greater transparency in algorithmic decision-making.
            
            Silicon Valley executives have expressed concern, warning that the rules could stifle innovation. "We share the goal of a fair digital marketplace, but these measures go too far," a spokesperson for a leading tech firm stated.
            
            Meanwhile, consumer advocacy groups have hailed the move as a necessary step to protect user privacy and ensure a level playing field for smaller competitors.""",
            
            """Scientists at NASA represent jubilant after the Perseverance rover successfully transmitted high-resolution panoramas of the Martian surface. The images reveal a rocky landscape that geologists believe was once home to an ancient river delta.
            
            "This is the clearest view we've ever had of this region," said Dr. Emily Chen, the mission's lead scientist. "The potential for discovering signs of past microbial life is higher than ever."
            
            The rover will now begin its journey toward the crater rim, collecting samples that will eventually be returned to Earth by a future mission."""
        ]

        self.stdout.write("Deleting old news...")
        News.objects.all().delete()

        self.stdout.write("Creating mock news...")
        for title in titles:
            content = random.choice(contents)
            # Add some variation to content length
            if random.random() > 0.5:
                content += "\n\n" + random.choice(contents)
                
            News.objects.create(
                title=title,
                content=content,
                created_at=timezone.now() - timezone.timedelta(days=random.randint(0, 10))
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(titles)} mock news articles'))
