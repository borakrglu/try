"""
Tarot Card Definitions - Complete 78-card deck with meanings
"""

from typing import Dict, List
from enum import Enum


class TarotSuit(str, Enum):
    """Tarot card suits"""
    MAJOR_ARCANA = "major_arcana"
    CUPS = "cups"
    WANDS = "wands"
    SWORDS = "swords"
    PENTACLES = "pentacles"


class TarotCard:
    """Represents a single tarot card"""

    def __init__(
        self,
        number: int,
        name: str,
        suit: TarotSuit,
        upright_keywords: List[str],
        reversed_keywords: List[str],
        upright_meaning: str,
        reversed_meaning: str,
        symbolism: str
    ):
        self.number = number
        self.name = name
        self.suit = suit
        self.upright_keywords = upright_keywords
        self.reversed_keywords = reversed_keywords
        self.upright_meaning = upright_meaning
        self.reversed_meaning = reversed_meaning
        self.symbolism = symbolism

    def to_dict(self, reversed: bool = False) -> Dict:
        """Convert card to dictionary format"""
        return {
            "number": self.number,
            "name": self.name,
            "suit": self.suit.value,
            "reversed": reversed,
            "keywords": self.reversed_keywords if reversed else self.upright_keywords,
            "meaning": self.reversed_meaning if reversed else self.upright_meaning,
            "symbolism": self.symbolism
        }


# Major Arcana (0-21)
MAJOR_ARCANA = [
    TarotCard(
        number=0,
        name="The Fool",
        suit=TarotSuit.MAJOR_ARCANA,
        upright_keywords=["New beginnings", "Innocence", "Spontaneity", "Free spirit"],
        reversed_keywords=["Recklessness", "Folly", "Naivety", "Poor judgment"],
        upright_meaning="The Fool represents new beginnings, having faith in the future, being inexperienced, not knowing what to expect, having beginner's luck, improvisation and believing in the universe.",
        reversed_meaning="The reversed Fool suggests acting foolishly, being gullible, or not taking things seriously enough. It warns against reckless behavior and poor judgment.",
        symbolism="Standing at the edge of a cliff with a small dog, white rose, and the sun above - symbolizing innocence, new journeys, and trust in the universe."
    ),
    TarotCard(
        number=1,
        name="The Magician",
        suit=TarotSuit.MAJOR_ARCANA,
        upright_keywords=["Manifestation", "Power", "Action", "Resourcefulness"],
        reversed_keywords=["Manipulation", "Illusion", "Untapped talents", "Trickery"],
        upright_meaning="The Magician represents manifestation, inspired action, and the ability to transform dreams into reality. You have all the tools you need to succeed.",
        reversed_meaning="The reversed Magician warns of manipulation, deception, or failing to manifest your goals due to lack of focus or misuse of power.",
        symbolism="Standing before a table with all four suit symbols (wands, cups, swords, pentacles), with infinity symbol above his head - representing unlimited potential."
    ),
    TarotCard(
        number=2,
        name="The High Priestess",
        suit=TarotSuit.MAJOR_ARCANA,
        upright_keywords=["Intuition", "Sacred knowledge", "Divine feminine", "Subconscious"],
        reversed_keywords=["Secrets", "Disconnected from intuition", "Withdrawal", "Silence"],
        upright_meaning="The High Priestess represents intuition, sacred knowledge, and the divine feminine. Trust your instincts and look beyond the obvious.",
        reversed_meaning="The reversed High Priestess suggests you're ignoring your intuition or keeping secrets. It's time to reconnect with your inner voice.",
        symbolism="Seated between two pillars (B and J) with the moon at her feet and Torah scroll - representing duality, mystery, and hidden wisdom."
    ),
    TarotCard(
        number=3,
        name="The Empress",
        suit=TarotSuit.MAJOR_ARCANA,
        upright_keywords=["Abundance", "Nurturing", "Fertility", "Divine feminine"],
        reversed_keywords=["Creative block", "Dependence", "Smothering", "Neglect"],
        upright_meaning="The Empress represents abundance, beauty, nature, and nurturing energy. A time of growth, creativity, and connection to the earth.",
        reversed_meaning="The reversed Empress warns of creative blocks, neglecting self-care, or being overly dependent on others for validation.",
        symbolism="Seated in nature surrounded by wheat and Venus symbol - representing fertility, abundance, and maternal care."
    ),
    TarotCard(
        number=4,
        name="The Emperor",
        suit=TarotSuit.MAJOR_ARCANA,
        upright_keywords=["Authority", "Structure", "Control", "Fatherhood"],
        reversed_keywords=["Domination", "Rigidity", "Lack of discipline", "Tyranny"],
        upright_meaning="The Emperor represents authority, structure, and solid foundation. Time to take control and establish order in your life.",
        reversed_meaning="The reversed Emperor warns of excessive control, rigidity, or abuse of power. Question authority and find balance.",
        symbolism="Seated on stone throne with ram heads and holding an ankh - representing leadership, stability, and worldly power."
    ),
    TarotCard(
        number=5,
        name="The Hierophant",
        suit=TarotSuit.MAJOR_ARCANA,
        upright_keywords=["Tradition", "Conformity", "Education", "Belief systems"],
        reversed_keywords=["Rebellion", "Breaking conventions", "New approaches", "Freedom"],
        upright_meaning="The Hierophant represents tradition, conformity, and spiritual wisdom. Seek guidance from established institutions or mentors.",
        reversed_meaning="The reversed Hierophant encourages breaking from tradition and finding your own path. Question dogma and embrace personal freedom.",
        symbolism="Religious figure between two pillars with crossed keys - representing spiritual authority, tradition, and conformity."
    ),
    TarotCard(
        number=6,
        name="The Lovers",
        suit=TarotSuit.MAJOR_ARCANA,
        upright_keywords=["Love", "Union", "Relationships", "Choices", "Harmony"],
        reversed_keywords=["Disharmony", "Imbalance", "Misalignment", "Self-love needed"],
        upright_meaning="The Lovers represent love, harmony, and important choices. A significant relationship or decision that aligns with your values.",
        reversed_meaning="The reversed Lovers warn of disharmony in relationships or choices that conflict with your values. Focus on self-love first.",
        symbolism="Adam and Eve with angel Raphael above - representing love, union, and the choices between heart and mind."
    ),
    TarotCard(
        number=7,
        name="The Chariot",
        suit=TarotSuit.MAJOR_ARCANA,
        upright_keywords=["Willpower", "Determination", "Success", "Control"],
        reversed_keywords=["Lack of direction", "Opposition", "Self-discipline needed"],
        upright_meaning="The Chariot represents determination, willpower, and victory. You have the focus and discipline to achieve your goals.",
        reversed_meaning="The reversed Chariot warns of lack of direction or being pulled in opposite directions. Regain control and focus.",
        symbolism="Warrior in chariot pulled by black and white sphinxes - representing victory through willpower and controlling opposing forces."
    ),
    TarotCard(
        number=8,
        name="Strength",
        suit=TarotSuit.MAJOR_ARCANA,
        upright_keywords=["Courage", "Inner strength", "Compassion", "Patience"],
        reversed_keywords=["Self-doubt", "Weakness", "Insecurity", "Low confidence"],
        upright_meaning="Strength represents inner strength, courage, and compassion. You have the power to overcome challenges through gentleness and patience.",
        reversed_meaning="The reversed Strength warns of self-doubt and lack of confidence. Reconnect with your inner power and overcome fear.",
        symbolism="Woman gently closing lion's mouth with infinity symbol above - representing courage, patience, and taming one's inner beast."
    ),
    TarotCard(
        number=9,
        name="The Hermit",
        suit=TarotSuit.MAJOR_ARCANA,
        upright_keywords=["Soul searching", "Introspection", "Inner guidance", "Solitude"],
        reversed_keywords=["Isolation", "Loneliness", "Withdrawal", "Lost your way"],
        upright_meaning="The Hermit represents soul searching, introspection, and inner guidance. Time to withdraw and seek answers within.",
        reversed_meaning="The reversed Hermit warns of excessive isolation or refusing guidance. Balance solitude with connection to others.",
        symbolism="Old man with lantern on mountain peak - representing wisdom, introspection, and the search for inner truth."
    ),
    TarotCard(
        number=10,
        name="Wheel of Fortune",
        suit=TarotSuit.MAJOR_ARCANA,
        upright_keywords=["Destiny", "Cycles", "Change", "Good luck"],
        reversed_keywords=["Bad luck", "Resistance to change", "Breaking cycles"],
        upright_meaning="The Wheel of Fortune represents destiny, life cycles, and turning points. Embrace change as the wheel turns in your favor.",
        reversed_meaning="The reversed Wheel warns of bad luck or resistance to inevitable change. Accept that some things are beyond your control.",
        symbolism="Wheel with four creatures and Egyptian symbols - representing karma, destiny, and the cyclical nature of life."
    ),
    TarotCard(
        number=11,
        name="Justice",
        suit=TarotSuit.MAJOR_ARCANA,
        upright_keywords=["Fairness", "Truth", "Law", "Cause and effect"],
        reversed_keywords=["Unfairness", "Dishonesty", "Lack of accountability"],
        upright_meaning="Justice represents fairness, truth, and cause and effect. Be prepared to accept responsibility and face consequences with integrity.",
        reversed_meaning="The reversed Justice warns of unfairness, dishonesty, or avoiding accountability. Seek truth and make amends.",
        symbolism="Figure seated between pillars holding sword and scales - representing balance, fairness, and karmic justice."
    ),
    TarotCard(
        number=12,
        name="The Hanged Man",
        suit=TarotSuit.MAJOR_ARCANA,
        upright_keywords=["Surrender", "New perspective", "Letting go", "Sacrifice"],
        reversed_keywords=["Stalling", "Needless sacrifice", "Fear of sacrifice"],
        upright_meaning="The Hanged Man represents surrender, letting go, and seeing things from a new perspective. Sometimes you must pause and sacrifice to move forward.",
        reversed_meaning="The reversed Hanged Man warns of stalling, resisting necessary change, or making needless sacrifices. Stop delaying.",
        symbolism="Man suspended upside-down from tree with serene expression - representing surrender, new perspectives, and willing sacrifice."
    ),
    TarotCard(
        number=13,
        name="Death",
        suit=TarotSuit.MAJOR_ARCANA,
        upright_keywords=["Endings", "Transformation", "Transition", "Letting go"],
        reversed_keywords=["Resistance to change", "Stagnation", "Fear of endings"],
        upright_meaning="Death represents transformation, endings, and new beginnings. Something must end for something new to begin - embrace the transition.",
        reversed_meaning="The reversed Death warns of resisting necessary change or clinging to the past. Accept endings as part of growth.",
        symbolism="Skeleton in armor on white horse with sun rising between towers - representing transformation, rebirth, and inevitable change."
    ),
    TarotCard(
        number=14,
        name="Temperance",
        suit=TarotSuit.MAJOR_ARCANA,
        upright_keywords=["Balance", "Moderation", "Patience", "Purpose"],
        reversed_keywords=["Imbalance", "Excess", "Self-indulgence", "Lack of harmony"],
        upright_meaning="Temperance represents balance, moderation, and patience. Find the middle path and blend opposing forces harmoniously.",
        reversed_meaning="The reversed Temperance warns of imbalance, excess, or lack of moderation. Restore harmony and practice patience.",
        symbolism="Angel pouring water between cups with one foot on land, one in water - representing balance, alchemy, and the middle path."
    ),
    TarotCard(
        number=15,
        name="The Devil",
        suit=TarotSuit.MAJOR_ARCANA,
        upright_keywords=["Bondage", "Addiction", "Materialism", "Shadow self"],
        reversed_keywords=["Release", "Freedom", "Breaking chains", "Detachment"],
        upright_meaning="The Devil represents bondage to material desires, addiction, or unhealthy attachments. Recognize your chains and seek freedom.",
        reversed_meaning="The reversed Devil signals release from bondage, breaking free from addiction, or overcoming limiting beliefs. Liberation is near.",
        symbolism="Horned figure with chained lovers below - representing temptation, materialism, and self-imposed bondage."
    ),
    TarotCard(
        number=16,
        name="The Tower",
        suit=TarotSuit.MAJOR_ARCANA,
        upright_keywords=["Sudden change", "Upheaval", "Chaos", "Revelation"],
        reversed_keywords=["Fear of change", "Avoiding disaster", "Delayed crisis"],
        upright_meaning="The Tower represents sudden upheaval, chaos, and revelation. Though disruptive, this breakdown clears the way for rebuilding on truth.",
        reversed_meaning="The reversed Tower suggests fear of inevitable change or narrowly avoiding disaster. Prepare for necessary transformation.",
        symbolism="Lightning striking tower with people falling - representing sudden revelation, destruction of false beliefs, and necessary chaos."
    ),
    TarotCard(
        number=17,
        name="The Star",
        suit=TarotSuit.MAJOR_ARCANA,
        upright_keywords=["Hope", "Renewal", "Inspiration", "Spirituality"],
        reversed_keywords=["Hopelessness", "Disconnection", "Lack of faith"],
        upright_meaning="The Star represents hope, renewal, and inspiration. After darkness comes light - trust in the universe and your path.",
        reversed_meaning="The reversed Star warns of hopelessness or disconnection from spirituality. Reconnect with faith and renew your spirit.",
        symbolism="Naked woman pouring water under stars - representing hope, renewal, and spiritual connection to the universe."
    ),
    TarotCard(
        number=18,
        name="The Moon",
        suit=TarotSuit.MAJOR_ARCANA,
        upright_keywords=["Illusion", "Intuition", "Unconscious", "Mystery"],
        reversed_keywords=["Clarity", "Release of fear", "Unhidden secrets"],
        upright_meaning="The Moon represents illusion, intuition, and the unconscious. Not all is as it seems - trust your intuition to navigate uncertainty.",
        reversed_meaning="The reversed Moon signals clarity emerging from confusion or release of fear. Secrets are revealed and illusions dispelled.",
        symbolism="Moon with face, dog and wolf howling, path to horizon - representing illusion, the unconscious, and the thin line between reality and fantasy."
    ),
    TarotCard(
        number=19,
        name="The Sun",
        suit=TarotSuit.MAJOR_ARCANA,
        upright_keywords=["Joy", "Success", "Vitality", "Positivity"],
        reversed_keywords=["Temporary depression", "Lack of success", "Sadness"],
        upright_meaning="The Sun represents joy, success, and vitality. Everything is illuminated - celebrate success and embrace positive energy.",
        reversed_meaning="The reversed Sun suggests temporary sadness or delayed success. The clouds will pass - maintain optimism.",
        symbolism="Large sun with child on white horse - representing joy, success, clarity, and pure positive energy."
    ),
    TarotCard(
        number=20,
        name="Judgement",
        suit=TarotSuit.MAJOR_ARCANA,
        upright_keywords=["Reflection", "Reckoning", "Awakening", "Absolution"],
        reversed_keywords=["Self-doubt", "Lack of self-awareness", "Refusal to learn"],
        upright_meaning="Judgement represents reflection, reckoning, and spiritual awakening. Time to evaluate your life and rise to a new level of consciousness.",
        reversed_meaning="The reversed Judgement warns of self-doubt or refusal to learn from past mistakes. Face yourself honestly and forgive.",
        symbolism="Angel Gabriel with trumpet, people rising from graves - representing judgment day, awakening, and the call to higher consciousness."
    ),
    TarotCard(
        number=21,
        name="The World",
        suit=TarotSuit.MAJOR_ARCANA,
        upright_keywords=["Completion", "Achievement", "Travel", "Success"],
        reversed_keywords=["Incompletion", "Delays", "Lack of closure"],
        upright_meaning="The World represents completion, achievement, and fulfillment. You've come full circle - celebrate your success and prepare for the next journey.",
        reversed_meaning="The reversed World warns of incompletion or lack of closure. Finish what you started before moving to the next cycle.",
        symbolism="Dancing figure in wreath with four creatures at corners - representing completion, unity, and the fulfillment of a major cycle."
    ),
]

# Minor Arcana - Cups (Emotions, Relationships, Creativity)
CUPS = [
    TarotCard(
        number=1, name="Ace of Cups", suit=TarotSuit.CUPS,
        upright_keywords=["New love", "Emotional renewal", "Creativity", "Compassion"],
        reversed_keywords=["Blocked emotions", "Emptiness", "Emotional loss"],
        upright_meaning="New emotional beginnings, overflowing love, creative inspiration, and spiritual connection.",
        reversed_meaning="Emotional blockages, repressed feelings, or disappointment in love.",
        symbolism="Overflowing chalice with dove - representing divine love and new emotional beginnings."
    ),
    TarotCard(
        number=2, name="Two of Cups", suit=TarotSuit.CUPS,
        upright_keywords=["Partnership", "Connection", "Attraction", "Unity"],
        reversed_keywords=["Imbalance", "Broken relationship", "Distrust"],
        upright_meaning="Partnership, mutual attraction, and balanced relationships.",
        reversed_meaning="Relationship imbalance, breakup, or lack of harmony.",
        symbolism="Two people exchanging cups with caduceus above."
    ),
    TarotCard(
        number=3, name="Three of Cups", suit=TarotSuit.CUPS,
        upright_keywords=["Celebration", "Friendship", "Community", "Joy"],
        reversed_keywords=["Overindulgence", "Gossip", "Isolation"],
        upright_meaning="Celebration, friendship, and joyful gatherings.",
        reversed_meaning="Overindulgence, gossip, or feeling isolated from friends.",
        symbolism="Three women raising cups in celebration."
    ),
    TarotCard(
        number=4, name="Four of Cups", suit=TarotSuit.CUPS,
        upright_keywords=["Apathy", "Contemplation", "Reevaluation", "Boredom"],
        reversed_keywords=["Awareness", "Acceptance", "Moving forward"],
        upright_meaning="Apathy, contemplation, and missing opportunities due to discontent.",
        reversed_meaning="Renewed awareness, acceptance, and readiness to move forward.",
        symbolism="Man under tree ignoring offered cup, focused on three cups before him."
    ),
    TarotCard(
        number=5, name="Five of Cups", suit=TarotSuit.CUPS,
        upright_keywords=["Loss", "Grief", "Disappointment", "Regret"],
        reversed_keywords=["Acceptance", "Moving on", "Finding peace"],
        upright_meaning="Loss, grief, and dwelling on disappointment.",
        reversed_meaning="Acceptance of loss and beginning to move forward.",
        symbolism="Figure mourning three spilled cups, two upright cups behind."
    ),
    TarotCard(
        number=6, name="Six of Cups", suit=TarotSuit.CUPS,
        upright_keywords=["Nostalgia", "Childhood", "Innocence", "Reunion"],
        reversed_keywords=["Living in past", "Naivety", "Unrealistic expectations"],
        upright_meaning="Nostalgia, happy memories, and innocent pleasures.",
        reversed_meaning="Stuck in the past or being unrealistic about relationships.",
        symbolism="Children exchanging flowers and cups in village setting."
    ),
    TarotCard(
        number=7, name="Seven of Cups", suit=TarotSuit.CUPS,
        upright_keywords=["Choices", "Fantasy", "Illusion", "Wishful thinking"],
        reversed_keywords=["Clarity", "Reality check", "Alignment"],
        upright_meaning="Multiple choices, fantasies, and potential illusions.",
        reversed_meaning="Gaining clarity and making realistic decisions.",
        symbolism="Figure before seven cups with various visions."
    ),
    TarotCard(
        number=8, name="Eight of Cups", suit=TarotSuit.CUPS,
        upright_keywords=["Walking away", "Seeking deeper meaning", "Letting go"],
        reversed_keywords=["Avoidance", "Fear of moving on", "Stagnation"],
        upright_meaning="Walking away from situations that no longer serve you.",
        reversed_meaning="Fear of change or avoiding necessary transitions.",
        symbolism="Figure walking away from eight cups toward mountains."
    ),
    TarotCard(
        number=9, name="Nine of Cups", suit=TarotSuit.CUPS,
        upright_keywords=["Contentment", "Satisfaction", "Wishes fulfilled"],
        reversed_keywords=["Dissatisfaction", "Greed", "Materialism"],
        upright_meaning="Emotional fulfillment, satisfaction, and wishes coming true.",
        reversed_meaning="Superficial satisfaction or never feeling satisfied.",
        symbolism="Satisfied figure sitting before nine cups."
    ),
    TarotCard(
        number=10, name="Ten of Cups", suit=TarotSuit.CUPS,
        upright_keywords=["Harmony", "Family bliss", "Alignment", "Happiness"],
        reversed_keywords=["Disharmony", "Broken family", "Disconnection"],
        upright_meaning="Emotional fulfillment, family happiness, and harmonious relationships.",
        reversed_meaning="Family discord, broken relationships, or misalignment in values.",
        symbolism="Family under rainbow of ten cups."
    ),
    TarotCard(
        number=11, name="Page of Cups", suit=TarotSuit.CUPS,
        upright_keywords=["Creative message", "Intuition", "Curiosity", "Possibility"],
        reversed_keywords=["Emotional immaturity", "Blocked creativity"],
        upright_meaning="Creative opportunities, intuitive messages, and emotional curiosity.",
        reversed_meaning="Emotional immaturity or creative blocks.",
        symbolism="Young person with fish emerging from cup."
    ),
    TarotCard(
        number=12, name="Knight of Cups", suit=TarotSuit.CUPS,
        upright_keywords=["Romance", "Charm", "Imagination", "Following heart"],
        reversed_keywords=["Moodiness", "Unrealistic", "Jealousy"],
        upright_meaning="Romantic gestures, following your heart, and creative pursuit.",
        reversed_meaning="Moodiness, unrealistic expectations, or emotional manipulation.",
        symbolism="Knight on white horse offering cup."
    ),
    TarotCard(
        number=13, name="Queen of Cups", suit=TarotSuit.CUPS,
        upright_keywords=["Compassion", "Intuition", "Emotional security"],
        reversed_keywords=["Emotional insecurity", "Codependency"],
        upright_meaning="Compassionate, intuitive, and emotionally mature energy.",
        reversed_meaning="Emotional insecurity, codependency, or being overly sensitive.",
        symbolism="Queen on throne by water holding ornate cup."
    ),
    TarotCard(
        number=14, name="King of Cups", suit=TarotSuit.CUPS,
        upright_keywords=["Emotional balance", "Diplomacy", "Compassion"],
        reversed_keywords=["Emotional manipulation", "Moodiness"],
        upright_meaning="Emotional maturity, wisdom, and balanced compassion.",
        reversed_meaning="Emotional manipulation, coldness, or mood swings.",
        symbolism="King on throne holding cup, surrounded by turbulent waters."
    ),
]

# Minor Arcana - Wands (Action, Energy, Passion, Ambition)
WANDS = [
    TarotCard(
        number=1, name="Ace of Wands", suit=TarotSuit.WANDS,
        upright_keywords=["Inspiration", "New opportunities", "Growth", "Potential"],
        reversed_keywords=["Delays", "Lack of direction", "Missed opportunities"],
        upright_meaning="Inspiration, new creative opportunities, and passionate beginnings.",
        reversed_meaning="Delays in projects, lack of direction, or missed opportunities.",
        symbolism="Hand from cloud holding sprouting wand."
    ),
    TarotCard(
        number=2, name="Two of Wands", suit=TarotSuit.WANDS,
        upright_keywords=["Planning", "Progress", "Decisions", "Discovery"],
        reversed_keywords=["Fear of unknown", "Lack of planning", "Disappointment"],
        upright_meaning="Planning for the future, making decisions, and personal power.",
        reversed_meaning="Fear of the unknown or poor planning.",
        symbolism="Figure holding globe looking out from castle."
    ),
    TarotCard(
        number=3, name="Three of Wands", suit=TarotSuit.WANDS,
        upright_keywords=["Expansion", "Foresight", "Progress", "Opportunities"],
        reversed_keywords=["Delays", "Obstacles", "Lack of progress"],
        upright_meaning="Expansion, foresight, and progress toward goals.",
        reversed_meaning="Delays, obstacles, or lack of forward movement.",
        symbolism="Figure overlooking ships from cliff."
    ),
    TarotCard(
        number=4, name="Four of Wands", suit=TarotSuit.WANDS,
        upright_keywords=["Celebration", "Harmony", "Marriage", "Home"],
        reversed_keywords=["Instability", "Lack of support", "Transition"],
        upright_meaning="Celebration, harmony, and achieving milestones.",
        reversed_meaning="Instability at home or lack of community support.",
        symbolism="Four wands with garland, people celebrating."
    ),
    TarotCard(
        number=5, name="Five of Wands", suit=TarotSuit.WANDS,
        upright_keywords=["Conflict", "Competition", "Disagreement"],
        reversed_keywords=["Resolution", "Agreement", "Avoiding conflict"],
        upright_meaning="Conflict, competition, and disagreement requiring resolution.",
        reversed_meaning="Conflict resolution or avoiding necessary confrontation.",
        symbolism="Five people with wands in mock battle."
    ),
    TarotCard(
        number=6, name="Six of Wands", suit=TarotSuit.WANDS,
        upright_keywords=["Victory", "Recognition", "Success", "Progress"],
        reversed_keywords=["Ego", "Lack of recognition", "Fall from grace"],
        upright_meaning="Victory, public recognition, and success.",
        reversed_meaning="Ego issues, lack of recognition, or temporary setback.",
        symbolism="Victorious rider on horse with wreath."
    ),
    TarotCard(
        number=7, name="Seven of Wands", suit=TarotSuit.WANDS,
        upright_keywords=["Defense", "Perseverance", "Maintaining position"],
        reversed_keywords=["Exhaustion", "Giving up", "Overwhelmed"],
        upright_meaning="Defending your position, perseverance, and standing your ground.",
        reversed_meaning="Feeling overwhelmed or giving up the fight.",
        symbolism="Figure on hill defending against six wands."
    ),
    TarotCard(
        number=8, name="Eight of Wands", suit=TarotSuit.WANDS,
        upright_keywords=["Speed", "Movement", "Quick action", "Progress"],
        reversed_keywords=["Delays", "Frustration", "Slowing down"],
        upright_meaning="Rapid action, movement, and swift progress.",
        reversed_meaning="Delays, frustration, or things slowing down.",
        symbolism="Eight wands flying through air."
    ),
    TarotCard(
        number=9, name="Nine of Wands", suit=TarotSuit.WANDS,
        upright_keywords=["Resilience", "Persistence", "Last stand"],
        reversed_keywords=["Exhaustion", "Paranoia", "Giving up"],
        upright_meaning="Resilience, persistence, and guarding what you've built.",
        reversed_meaning="Exhaustion, paranoia, or being close to breaking point.",
        symbolism="Wounded figure leaning on wand, eight wands behind."
    ),
    TarotCard(
        number=10, name="Ten of Wands", suit=TarotSuit.WANDS,
        upright_keywords=["Burden", "Responsibility", "Stress", "Burnout"],
        reversed_keywords=["Release", "Delegation", "Lightening load"],
        upright_meaning="Heavy burden, too many responsibilities, and approaching burnout.",
        reversed_meaning="Releasing burdens, delegating, or lightening your load.",
        symbolism="Figure carrying ten heavy wands."
    ),
    TarotCard(
        number=11, name="Page of Wands", suit=TarotSuit.WANDS,
        upright_keywords=["Enthusiasm", "Exploration", "Discovery", "Free spirit"],
        reversed_keywords=["Lack of direction", "Procrastination", "Immaturity"],
        upright_meaning="Enthusiastic messenger, new ventures, and exploration.",
        reversed_meaning="Lack of direction or inability to commit to projects.",
        symbolism="Young person holding wand, looking at it with curiosity."
    ),
    TarotCard(
        number=12, name="Knight of Wands", suit=TarotSuit.WANDS,
        upright_keywords=["Energy", "Passion", "Adventure", "Impulsiveness"],
        reversed_keywords=["Recklessness", "Impatience", "Hasty decisions"],
        upright_meaning="Passionate action, adventure, and energetic pursuit of goals.",
        reversed_meaning="Recklessness, impatience, or hasty decisions.",
        symbolism="Knight on rearing horse with wand raised."
    ),
    TarotCard(
        number=13, name="Queen of Wands", suit=TarotSuit.WANDS,
        upright_keywords=["Confidence", "Independence", "Determination", "Vibrancy"],
        reversed_keywords=["Jealousy", "Insecurity", "Selfishness"],
        upright_meaning="Confident, independent, and passionate leadership.",
        reversed_meaning="Jealousy, insecurity, or domineering behavior.",
        symbolism="Queen on throne holding wand and sunflower, black cat beside."
    ),
    TarotCard(
        number=14, name="King of Wands", suit=TarotSuit.WANDS,
        upright_keywords=["Leadership", "Vision", "Entrepreneur", "Honor"],
        reversed_keywords=["Arrogance", "Impulsiveness", "Ruthless"],
        upright_meaning="Natural leader, visionary, and entrepreneurial spirit.",
        reversed_meaning="Arrogance, impulsiveness, or abusing power.",
        symbolism="King on throne holding flowering wand, lions on throne."
    ),
]

# Minor Arcana - Swords (Intellect, Conflict, Communication, Truth)
SWORDS = [
    TarotCard(
        number=1, name="Ace of Swords", suit=TarotSuit.SWORDS,
        upright_keywords=["Clarity", "Breakthrough", "New ideas", "Mental clarity"],
        reversed_keywords=["Confusion", "Chaos", "Lack of clarity"],
        upright_meaning="Mental clarity, breakthrough ideas, and new perspectives.",
        reversed_meaning="Confusion, chaos, or clouded judgment.",
        symbolism="Hand from cloud holding upright sword with crown."
    ),
    TarotCard(
        number=2, name="Two of Swords", suit=TarotSuit.SWORDS,
        upright_keywords=["Difficult choices", "Stalemate", "Avoidance"],
        reversed_keywords=["Decision made", "Information revealed"],
        upright_meaning="Difficult choices, indecision, and avoiding truth.",
        reversed_meaning="Breaking stalemate and making a decision.",
        symbolism="Blindfolded figure holding two crossed swords."
    ),
    TarotCard(
        number=3, name="Three of Swords", suit=TarotSuit.SWORDS,
        upright_keywords=["Heartbreak", "Sorrow", "Grief", "Pain"],
        reversed_keywords=["Healing", "Forgiveness", "Recovery"],
        upright_meaning="Heartbreak, emotional pain, and sorrow.",
        reversed_meaning="Healing from heartbreak and moving forward.",
        symbolism="Heart pierced by three swords."
    ),
    TarotCard(
        number=4, name="Four of Swords", suit=TarotSuit.SWORDS,
        upright_keywords=["Rest", "Recuperation", "Meditation", "Contemplation"],
        reversed_keywords=["Restlessness", "Burnout", "Stagnation"],
        upright_meaning="Rest, recuperation, and quiet contemplation.",
        reversed_meaning="Restlessness, burnout, or forced rest.",
        symbolism="Knight resting on tomb with three swords above."
    ),
    TarotCard(
        number=5, name="Five of Swords", suit=TarotSuit.SWORDS,
        upright_keywords=["Conflict", "Defeat", "Win at all costs", "Betrayal"],
        reversed_keywords=["Reconciliation", "Making amends", "Moving on"],
        upright_meaning="Conflict, defeat, and hollow victories.",
        reversed_meaning="Reconciliation and making amends after conflict.",
        symbolism="Figure collecting swords while others walk away defeated."
    ),
    TarotCard(
        number=6, name="Six of Swords", suit=TarotSuit.SWORDS,
        upright_keywords=["Transition", "Moving on", "Leaving behind"],
        reversed_keywords=["Resistance to change", "Unfinished business"],
        upright_meaning="Transition to calmer waters and leaving troubles behind.",
        reversed_meaning="Resistance to necessary change or unfinished business.",
        symbolism="Boat carrying passengers and six swords to calmer waters."
    ),
    TarotCard(
        number=7, name="Seven of Swords", suit=TarotSuit.SWORDS,
        upright_keywords=["Deception", "Strategy", "Sneakiness", "Betrayal"],
        reversed_keywords=["Truth revealed", "Regret", "Confession"],
        upright_meaning="Deception, sneaky behavior, or strategic retreat.",
        reversed_meaning="Truth coming to light or feeling guilty about actions.",
        symbolism="Figure sneaking away with five swords, leaving two behind."
    ),
    TarotCard(
        number=8, name="Eight of Swords", suit=TarotSuit.SWORDS,
        upright_keywords=["Trapped", "Victimhood", "Self-imposed restriction"],
        reversed_keywords=["Freedom", "Release", "Self-acceptance"],
        upright_meaning="Feeling trapped by circumstances or self-imposed limitations.",
        reversed_meaning="Breaking free from restrictions and finding freedom.",
        symbolism="Blindfolded bound figure surrounded by eight swords."
    ),
    TarotCard(
        number=9, name="Nine of Swords", suit=TarotSuit.SWORDS,
        upright_keywords=["Anxiety", "Worry", "Nightmares", "Fear"],
        reversed_keywords=["Hope", "Recovery", "Facing fears"],
        upright_meaning="Anxiety, worry, and mental anguish.",
        reversed_meaning="Hope returning and beginning to face fears.",
        symbolism="Figure sitting up in bed with nine swords on wall."
    ),
    TarotCard(
        number=10, name="Ten of Swords", suit=TarotSuit.SWORDS,
        upright_keywords=["Rock bottom", "Crisis", "Betrayal", "Endings"],
        reversed_keywords=["Recovery", "Regeneration", "Worst is over"],
        upright_meaning="Rock bottom, painful endings, and complete defeat.",
        reversed_meaning="Recovery beginning, worst is over, and regeneration.",
        symbolism="Figure face down with ten swords in back, dawn approaching."
    ),
    TarotCard(
        number=11, name="Page of Swords", suit=TarotSuit.SWORDS,
        upright_keywords=["Curiosity", "Mental energy", "Vigilance", "New ideas"],
        reversed_keywords=["Gossip", "Deception", "All talk no action"],
        upright_meaning="Curious mind, new ideas, and vigilant communication.",
        reversed_meaning="Gossip, deception, or failing to follow through on ideas.",
        symbolism="Young person holding sword aloft with wind blowing."
    ),
    TarotCard(
        number=12, name="Knight of Swords", suit=TarotSuit.SWORDS,
        upright_keywords=["Action", "Assertiveness", "Driven", "Quick thinking"],
        reversed_keywords=["Impulsive", "Aggressive", "Reckless"],
        upright_meaning="Swift action, assertive communication, and driven pursuit.",
        reversed_meaning="Impulsiveness, aggression, or reckless behavior.",
        symbolism="Knight charging forward on horse with raised sword."
    ),
    TarotCard(
        number=13, name="Queen of Swords", suit=TarotSuit.SWORDS,
        upright_keywords=["Independent", "Clear thinking", "Direct communication"],
        reversed_keywords=["Cold", "Bitter", "Cruel"],
        upright_meaning="Independent thinker with clear, direct communication.",
        reversed_meaning="Coldness, bitterness, or cruel honesty.",
        symbolism="Queen on throne holding upright sword and extending hand."
    ),
    TarotCard(
        number=14, name="King of Swords", suit=TarotSuit.SWORDS,
        upright_keywords=["Authority", "Truth", "Intellectual power", "Clarity"],
        reversed_keywords=["Manipulation", "Tyranny", "Abusive power"],
        upright_meaning="Intellectual authority, truth, and clear judgment.",
        reversed_meaning="Manipulation, abuse of power, or tyrannical behavior.",
        symbolism="King on throne holding upright sword with stern expression."
    ),
]

# Minor Arcana - Pentacles (Material, Finance, Career, Physical)
PENTACLES = [
    TarotCard(
        number=1, name="Ace of Pentacles", suit=TarotSuit.PENTACLES,
        upright_keywords=["Opportunity", "Prosperity", "New venture", "Manifestation"],
        reversed_keywords=["Lost opportunity", "Lack of planning", "Materialism"],
        upright_meaning="New financial opportunity, prosperity, and material manifestation.",
        reversed_meaning="Lost opportunity or poor financial planning.",
        symbolism="Hand from cloud holding golden pentacle over garden."
    ),
    TarotCard(
        number=2, name="Two of Pentacles", suit=TarotSuit.PENTACLES,
        upright_keywords=["Balance", "Adaptability", "Juggling", "Flexibility"],
        reversed_keywords=["Imbalance", "Disorganization", "Overwhelmed"],
        upright_meaning="Balancing multiple priorities and staying flexible.",
        reversed_meaning="Loss of balance or being overwhelmed by responsibilities.",
        symbolism="Figure juggling two pentacles in infinity loop."
    ),
    TarotCard(
        number=3, name="Three of Pentacles", suit=TarotSuit.PENTACLES,
        upright_keywords=["Teamwork", "Collaboration", "Building", "Learning"],
        reversed_keywords=["Lack of teamwork", "Disharmony", "Poor quality"],
        upright_meaning="Teamwork, collaboration, and building something together.",
        reversed_meaning="Lack of teamwork or poor quality work.",
        symbolism="Craftsperson working with two others in cathedral."
    ),
    TarotCard(
        number=4, name="Four of Pentacles", suit=TarotSuit.PENTACLES,
        upright_keywords=["Security", "Control", "Conservation", "Possessiveness"],
        reversed_keywords=["Greed", "Materialism", "Self-protection"],
        upright_meaning="Financial security, control, and material conservation.",
        reversed_meaning="Greed, materialism, or excessive control.",
        symbolism="Figure holding pentacle tightly, sitting on pentacles."
    ),
    TarotCard(
        number=5, name="Five of Pentacles", suit=TarotSuit.PENTACLES,
        upright_keywords=["Financial loss", "Hardship", "Isolation", "Worry"],
        reversed_keywords=["Recovery", "Improvement", "Seeking help"],
        upright_meaning="Financial hardship, feeling left out in the cold.",
        reversed_meaning="Recovery from hardship and accepting help.",
        symbolism="Two figures in snow passing lit church window."
    ),
    TarotCard(
        number=6, name="Six of Pentacles", suit=TarotSuit.PENTACLES,
        upright_keywords=["Generosity", "Charity", "Giving", "Sharing"],
        reversed_keywords=["Strings attached", "Debt", "Imbalanced giving"],
        upright_meaning="Generosity, charity, and sharing wealth.",
        reversed_meaning="One-sided generosity or strings attached to giving.",
        symbolism="Wealthy figure giving coins to beggars with scales."
    ),
    TarotCard(
        number=7, name="Seven of Pentacles", suit=TarotSuit.PENTACLES,
        upright_keywords=["Assessment", "Patience", "Long-term view", "Perseverance"],
        reversed_keywords=["Impatience", "Lack of progress", "Frustration"],
        upright_meaning="Assessing progress, patience, and long-term investment.",
        reversed_meaning="Impatience with results or frustration with slow progress.",
        symbolism="Farmer resting on tool, looking at pentacle bush."
    ),
    TarotCard(
        number=8, name="Eight of Pentacles", suit=TarotSuit.PENTACLES,
        upright_keywords=["Skill development", "Hard work", "Dedication", "Craftsmanship"],
        reversed_keywords=["Lack of focus", "Perfectionism", "Mediocrity"],
        upright_meaning="Skill development, dedication to craft, and hard work.",
        reversed_meaning="Lack of focus or perfectionism preventing progress.",
        symbolism="Craftsperson carefully creating pentacles."
    ),
    TarotCard(
        number=9, name="Nine of Pentacles", suit=TarotSuit.PENTACLES,
        upright_keywords=["Independence", "Luxury", "Self-sufficiency", "Success"],
        reversed_keywords=["Overspending", "Dependence", "Work-life imbalance"],
        upright_meaning="Financial independence, luxury, and self-sufficiency.",
        reversed_meaning="Overspending or sacrificing too much for success.",
        symbolism="Wealthy figure in vineyard with bird."
    ),
    TarotCard(
        number=10, name="Ten of Pentacles", suit=TarotSuit.PENTACLES,
        upright_keywords=["Wealth", "Legacy", "Family", "Long-term success"],
        reversed_keywords=["Financial failure", "Family disputes", "Debt"],
        upright_meaning="Wealth, family legacy, and long-term financial success.",
        reversed_meaning="Financial problems or family disputes over money.",
        symbolism="Multi-generational family with ten pentacles showing inheritance."
    ),
    TarotCard(
        number=11, name="Page of Pentacles", suit=TarotSuit.PENTACLES,
        upright_keywords=["Opportunity", "Study", "New project", "Manifestation"],
        reversed_keywords=["Procrastination", "Lack of progress", "Distraction"],
        upright_meaning="New financial opportunity, study, or practical project.",
        reversed_meaning="Procrastination or lack of follow-through on opportunities.",
        symbolism="Young person studying pentacle with focus."
    ),
    TarotCard(
        number=12, name="Knight of Pentacles", suit=TarotSuit.PENTACLES,
        upright_keywords=["Efficiency", "Responsibility", "Routine", "Conservatism"],
        reversed_keywords=["Laziness", "Boredom", "Stuck in routine"],
        upright_meaning="Efficient, responsible, and methodical approach to work.",
        reversed_meaning="Laziness, boredom, or being stuck in rut.",
        symbolism="Knight on stationary horse holding pentacle."
    ),
    TarotCard(
        number=13, name="Queen of Pentacles", suit=TarotSuit.PENTACLES,
        upright_keywords=["Nurturing", "Practical", "Abundance", "Down-to-earth"],
        reversed_keywords=["Self-care neglect", "Work-life imbalance"],
        upright_meaning="Nurturing, practical abundance, and grounded wisdom.",
        reversed_meaning="Neglecting self-care or work-life imbalance.",
        symbolism="Queen on throne in nature holding large pentacle."
    ),
    TarotCard(
        number=14, name="King of Pentacles", suit=TarotSuit.PENTACLES,
        upright_keywords=["Wealth", "Business success", "Security", "Abundance"],
        reversed_keywords=["Greed", "Materialistic", "Financial instability"],
        upright_meaning="Financial success, business acumen, and material abundance.",
        reversed_meaning="Greed, materialism, or poor financial management.",
        symbolism="King on throne surrounded by vines holding pentacle."
    ),
]

# Complete deck
ALL_CARDS = MAJOR_ARCANA + CUPS + WANDS + SWORDS + PENTACLES


def get_all_cards() -> List[TarotCard]:
    """Get all 78 tarot cards"""
    return ALL_CARDS


def get_cards_by_suit(suit: TarotSuit) -> List[TarotCard]:
    """Get all cards of a specific suit"""
    return [card for card in ALL_CARDS if card.suit == suit]


def get_card_by_name(name: str) -> TarotCard:
    """Get a specific card by name"""
    for card in ALL_CARDS:
        if card.name.lower() == name.lower():
            return card
    raise ValueError(f"Card '{name}' not found")


def get_random_cards(count: int = 1, allow_duplicates: bool = False) -> List[tuple[TarotCard, bool]]:
    """
    Get random cards for a reading

    Args:
        count: Number of cards to draw
        allow_duplicates: Whether to allow the same card multiple times

    Returns:
        List of tuples (card, is_reversed)
    """
    import random

    if count > 78 and not allow_duplicates:
        raise ValueError("Cannot draw more than 78 unique cards")

    if allow_duplicates:
        cards = [random.choice(ALL_CARDS) for _ in range(count)]
    else:
        cards = random.sample(ALL_CARDS, count)

    # Randomly determine if each card is reversed (40% chance)
    return [(card, random.random() < 0.4) for card in cards]
