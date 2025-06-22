class PersonalityInterpreter:
    def __init__(self):
        # Thresholds for trait levels
        self.thresholds = {
            'low': 0.35,
            'high': 0.65
        }

        # Personality descriptions based on OCEAN traits
        self.trait_descriptions = {
            'extraversion': {
                'low': [
                    "tends to be quiet and reserved in social settings",
                    "draws energy from solitude and deep one-on-one connections",
                    "values their personal space and time for introspection",
                    "prefers smaller, intimate gatherings to large social events",
                    "thinks carefully before speaking and values meaningful conversation"
                ],
                'medium': [
                    "balances social time with personal space effectively",
                    "can engage socially when needed but also values alone time",
                    "adapts their social energy depending on the situation",
                    "enjoys both group activities and solitary pursuits",
                    "can lead when necessary but doesn't always seek the spotlight"
                ],
                'high': [
                    "thrives in social situations and enjoys meeting new people",
                    "is energetic and enthusiastic in their interactions",
                    "seeks out excitement and stimulating environments",
                    "communicates expressively and shares thoughts readily",
                    "naturally takes charge in group settings"
                ]
            },
            'neuroticism': {
                'low': [
                    "maintains emotional stability even under pressure",
                    "approaches challenges with a calm and steady mindset",
                    "recovers quickly from setbacks and disappointments",
                    "tends to stay optimistic in difficult situations",
                    "rarely becomes overwhelmed by stress or anxiety"
                ],
                'medium': [
                    "experiences a normal range of emotional ups and downs",
                    "generally handles stress well but may occasionally feel overwhelmed",
                    "is reasonably resilient while still being emotionally responsive",
                    "can usually manage anxiety though sometimes needs time to process",
                    "balances realistic concerns with positive outlook"
                ],
                'high': [
                    "experiences emotions intensely and may worry frequently",
                    "is highly sensitive to stress and environmental changes",
                    "tends to analyze situations deeply, sometimes leading to overthinking",
                    "may struggle with anxiety when facing uncertain situations",
                    "feels emotions deeply and processes experiences thoroughly"
                ]
            },
            'agreeableness': {
                'low': [
                    "prioritizes logical thinking over emotional considerations",
                    "isn't afraid to challenge others' opinions when necessary",
                    "values honesty and directness in communication",
                    "approaches decisions with analytical reasoning",
                    "maintains strong boundaries and stands firm in their positions"
                ],
                'medium': [
                    "balances cooperation with standing up for their own needs",
                    "can be diplomatic while still expressing honest opinions",
                    "shows compassion while maintaining healthy boundaries",
                    "considers others' feelings without sacrificing their own priorities",
                    "cooperates well but can be assertive when values are compromised"
                ],
                'high': [
                    "genuinely cares about others' wellbeing and happiness",
                    "approaches conflicts with empathy and understanding",
                    "readily offers help and support to those in need",
                    "values harmony and cooperation in relationships",
                    "shows compassion and consideration in their interactions"
                ]
            },
            'conscientiousness': {
                'low': [
                    "takes a flexible and spontaneous approach to life",
                    "adapts quickly to changing circumstances",
                    "prefers to keep options open rather than make rigid plans",
                    "tackles tasks with creative, outside-the-box thinking",
                    "values freedom and resists excessive structure"
                ],
                'medium': [
                    "maintains a balance between organization and flexibility",
                    "can follow plans while adapting to unexpected changes",
                    "is reasonably reliable while avoiding excessive rigidity",
                    "sets goals but remains open to adjusting priorities",
                    "appreciates both spontaneity and structure in appropriate contexts"
                ],
                'high': [
                    "approaches tasks with careful planning and organization",
                    "demonstrates strong self-discipline and work ethic",
                    "pays close attention to details and quality",
                    "follows through on commitments reliably",
                    "sets clear goals and works persistently to achieve them"
                ]
            },
            'openness': {
                'low': [
                    "values practical thinking and concrete solutions",
                    "appreciates tradition and time-tested approaches",
                    "prefers familiar routines and established methods",
                    "focuses on tangible realities rather than abstract concepts",
                    "takes a pragmatic approach to life's challenges"
                ],
                'medium': [
                    "balances traditional approaches with occasional new ideas",
                    "appreciates both practical solutions and creative thinking",
                    "explores new concepts while maintaining some familiar routines",
                    "shows moderate curiosity about different perspectives",
                    "can appreciate both abstract and concrete thinking"
                ],
                'high': [
                    "shows deep curiosity and interest in novel experiences",
                    "thinks creatively and appreciates abstract ideas",
                    "actively seeks out different perspectives and worldviews",
                    "enjoys exploring complex questions and philosophical discussions",
                    "embraces change and values innovation"
                ]
            }
        }

        # Dynamic personality insights based on trait combinations
        self.combination_insights = [
            # High extraversion combinations
            {
                'conditions': {'extraversion': 'high', 'openness': 'high'},
                'insight': "thrives on novelty and social exploration, likely seeking out unique experiences to share with others"
            },
            {
                'conditions': {'extraversion': 'high', 'conscientiousness': 'high'},
                'insight': "combines social leadership with reliable follow-through, making them effective in organizing group activities"
            },
            {
                'conditions': {'extraversion': 'high', 'agreeableness': 'high'},
                'insight': "creates warm social connections easily and helps maintain group harmony"
            },
            {
                'conditions': {'extraversion': 'high', 'neuroticism': 'low'},
                'insight': "brings confident energy to social situations and maintains optimism under pressure"
            },

            # Low extraversion combinations
            {
                'conditions': {'extraversion': 'low', 'openness': 'high'},
                'insight': "may prefer exploring ideas through reading, art, or deep one-on-one conversations rather than group activities"
            },
            {
                'conditions': {'extraversion': 'low', 'conscientiousness': 'high'},
                'insight': "works effectively on independent projects requiring focus and attention to detail"
            },

            # High openness combinations
            {
                'conditions': {'openness': 'high', 'conscientiousness': 'high'},
                'insight': "channels creativity through structured approaches, likely setting and achieving innovative goals"
            },
            {
                'conditions': {'openness': 'high', 'agreeableness': 'low'},
                'insight': "may challenge conventional thinking directly, valuing intellectual honesty over social harmony"
            },

            # High conscientiousness combinations
            {
                'conditions': {'conscientiousness': 'high', 'neuroticism': 'high'},
                'insight': "may set high personal standards and feel stress when unable to meet them perfectly"
            },
            {
                'conditions': {'conscientiousness': 'high', 'agreeableness': 'high'},
                'insight': "reliably follows through on commitments to others, making them a dependable friend and colleague"
            },

            # High agreeableness combinations
            {
                'conditions': {'agreeableness': 'high', 'neuroticism': 'high'},
                'insight': "deeply cares about relationships and may worry about others' perceptions and needs"
            },

            # Low conscientiousness combinations
            {
                'conditions': {'conscientiousness': 'low', 'openness': 'high'},
                'insight': "approaches life with spontaneous creativity, preferring exploration over rigid planning"
            },

            # More complex combinations
            {
                'conditions': {'extraversion': 'high', 'openness': 'high', 'conscientiousness': 'low'},
                'insight': "seeks out novel social experiences and adventures, preferring spontaneity over detailed planning"
            },
            {
                'conditions': {'agreeableness': 'high', 'conscientiousness': 'high', 'neuroticism': 'low'},
                'insight': "creates stable, harmonious environments through reliable action and emotional steadiness"
            },
            {
                'conditions': {'extraversion': 'low', 'openness': 'low', 'conscientiousness': 'high'},
                'insight': "works diligently within established systems, valuing reliability and tradition"
            }
        ]

        # Relationship and career insights
        self.life_insights = {
            'relationships': {
                'extraversion': {
                    'high': "seeks active social connections and shared activities in relationships",
                    'low': "values deep, meaningful connections with a smaller circle of close relationships"
                },
                'neuroticism': {
                    'high': "appreciates partners who provide emotional support and understanding",
                    'low': "brings stability and calm to relationships, especially during challenges"
                },
                'agreeableness': {
                    'high': "prioritizes harmony and tends to be accommodating in relationships",
                    'low': "values straightforward communication and honest exchanges"
                },
                'conscientiousness': {
                    'high': "is reliable and committed in relationships, following through on promises",
                    'low': "brings spontaneity and flexibility to relationships"
                },
                'openness': {
                    'high': "enjoys exploring new experiences and intellectual discussions with partners",
                    'low': "provides stability and appreciates established routines in relationships"
                }
            },
            'career': {
                'extraversion': {
                    'high': "may thrive in roles involving teamwork, leadership, or customer interaction",
                    'low': "often excels in positions requiring concentration, deep focus, or independent work"
                },
                'neuroticism': {
                    'high': "may perform well in detail-oriented roles where thoroughness is valued",
                    'low': "typically handles high-pressure situations effectively and adapts to change"
                },
                'agreeableness': {
                    'high': "often finds fulfillment in helping professions or collaborative environments",
                    'low': "may excel in roles requiring critical analysis, negotiation, or competition"
                },
                'conscientiousness': {
                    'high': "tends to perform well in structured environments requiring reliability and organization",
                    'low': "may thrive in dynamic settings requiring adaptability and quick responses"
                },
                'openness': {
                    'high': "often enjoys creative fields, research, or positions involving innovation",
                    'low': "may excel in practical fields where consistency and concrete thinking are valued"
                }
            }
        }

    def get_trait_level(self, score):
        """Determine if a trait score is low, medium, or high."""
        if score < self.thresholds['low']:
            return 'low'
        elif score > self.thresholds['high']:
            return 'high'
        else:
            return 'medium'

    def get_trait_description(self, trait, score):
        """Get a random description for a trait based on its level."""
        level = self.get_trait_level(score)
        descriptions = self.trait_descriptions[trait][level]
        # Using index calculation instead of hash to avoid potential issues
        index = int((score * 100) % len(descriptions))
        return descriptions[index]

    def get_combination_insights(self, trait_levels):
        """Find relevant combination insights based on trait levels."""
        insights = []

        for combo in self.combination_insights:
            matches = True
            for trait, level in combo['conditions'].items():
                if trait_levels[trait] != level:
                    matches = False
                    break

            if matches:
                insights.append(combo['insight'])

        # Return up to 3 insights to avoid overwhelming the user
        return insights[:3]

    def get_life_insights(self, trait_levels):
        """Get relationship and career insights based on trait levels."""
        relationship_insights = []
        career_insights = []

        # Create a list of traits with their numeric distance from 0.5 (middle)
        # First convert trait levels to numeric values for sorting
        trait_values = {
            'low': 0.25,
            'medium': 0.5,
            'high': 0.75
        }

        # Convert string levels to numeric values for sorting
        numeric_trait_levels = [(trait, trait_values[level]) for trait, level in trait_levels.items()]

        # Sort by how extreme they are (distance from middle value 0.5)
        sorted_traits = sorted(numeric_trait_levels, key=lambda x: abs(0.5 - x[1]), reverse=True)[:2]

        # Convert back to original string levels for insight lookup
        for trait, _ in sorted_traits:
            level = trait_levels[trait]
            if level != 'medium':  # Only include insights for high or low traits
                relationship_insights.append(self.life_insights['relationships'][trait][level])
                career_insights.append(self.life_insights['career'][trait][level])

        return {
            'relationships': relationship_insights,
            'career': career_insights
        }

    def generate_personality_summary(self, average_scores):
        """Generate a comprehensive personality summary based on OCEAN scores."""
        # Convert scores to trait levels (low, medium, high)
        trait_levels = {trait: self.get_trait_level(score) for trait, score in average_scores.items()}

        # Get individual trait descriptions
        trait_descriptions = {trait: self.get_trait_description(trait, score)
                              for trait, score in average_scores.items()}

        # Get combination insights
        combination_insights = self.get_combination_insights(trait_levels)

        # Get life insights
        life_insights = self.get_life_insights(trait_levels)

        # Create summary
        summary = ["Based on the analyzed text, this personality profile reveals someone who:"]

        # Add individual trait descriptions
        for trait, description in trait_descriptions.items():
            summary.append(f"• {description}")

        # Add combination insights if available
        if combination_insights:
            summary.append("\nAdditional insights:")
            for insight in combination_insights:
                summary.append(f"• This person {insight}")

        # Add relationship insights
        if life_insights['relationships']:
            summary.append("\nIn relationships, this person likely:")
            for insight in life_insights['relationships']:
                summary.append(f"• {insight}")

        # Add career insights
        if life_insights['career']:
            summary.append("\nIn work environments, this person typically:")
            for insight in life_insights['career']:
                summary.append(f"• {insight}")

        # Final note on interpretation
        summary.append(
            "\nNote: This analysis is based on writing style and word choice patterns. For a complete personality assessment, professional evaluation is recommended.")

        return "\n".join(summary)
