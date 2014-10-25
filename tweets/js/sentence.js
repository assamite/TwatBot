/*
 * main.js
 * 
 * New Age Bullshit Generator
 * (C) 2014 Seb Pearce (sebpearce.com)
 * Licensed under the MIT License.
 * 
 * Modified by Simo Linkola (2014).
 * 
 */

var nEnergy = [
   'power',
   'energy',
   'radiation',
   'vibration',
   'entanglement',
   'force',
   'meaning',
   'purpose',
   'knowledge'
]

var nCosmos = [
  'cosmos',
  'quantum soup',
  'infinite',
  'universe',
  'galaxy',
  'multiverse',
  'grid',
  'quantum matrix',
  'totality',
  'quantum cycle',
  'nexus',
  'planet',
  'solar system',
  'world',
  'stratosphere',
  'dreamscape',
  'biosphere',
  'space',
  'reality'
];

var nPerson = [
  'being',
  'child',
  'traveller',
  'entity',
  'lifeform',
  'wanderer',
  'visitor',
  'prophet',
  'seeker',
  'soul',
  'healer',
  'sage',
  'shaman'
];

var nPersonPlural = [
  'beings',
  // 'children',
  'travellers',
  'entities',
  'lifeforms',
  'dreamweavers',
  'adventurers',
  'pilgrims',
  'warriors',
  'messengers',
  'dreamers',
  'storytellers',
  'seekers',
  'healers',
  'sages',
  'shamans'
];

var nMass = [
  'consciousness',
  'nature',
  'beauty',
  'knowledge',
  'truth',
  'life',
  'healing',
  'potential',
  'freedom',
  'purpose',
  'coherence',
  'choice',
  'passion',
  'understanding',
  'balance',
  'growth',
  'inspiration',
  'conscious living',
  'energy',
  'health',
  'spacetime',
  'learning',
  'being',
  'wisdom',
  'stardust',
  'sharing',
  'science',
  'curiosity',
  'hope',
  'wonder',
  'faith',
  'fulfillment',
  'peace',
  'rebirth',
  'self-actualization',
  'presence',
  'power',
  'will',
  'flow',
  'potential',
  'potentiality',
  'chi',
  'intuition',
  'synchronicity',
  'wellbeing',
  'joy',
  'love',
  'karma',
  'life-force',
  'awareness',
  'guidance',
  'transformation',
  'grace',
  'divinity',
  'non-locality',
  'inseparability',
  'interconnectedness',
  'transcendence',
  'empathy',
  'insight',
  'rejuvenation',
  'ecstasy',
  'aspiration',
  'complexity',
  'serenity'
];

var nMassBad = [
  'turbulence',
  'pain',
  'suffering',
  'stagnation',
  'desire',
  'greed',
  'selfishness',
  'ego',
  'dogma',
  'illusion',
  'delusion',
  'yearning',
  'discontinuity',
  'materialism'
];

var nOurPlural = [
  'souls',
  'lives',
  'dreams',
  'hopes',
  'bodies',
  'hearts',
  'brains',
  'third eyes',
  'essences',
  'chakras'
];

var nPath = [
  'circuit',
  'mission',
  'journey',
  'path',
  'quest',
  'vision quest',
  'story',
  'myth'
];

var nOf = [
  'quantum leap',
  'evolution',
  'spark',
  'lightning bolt',
  'reintegration',
  'vector',
  'rebirth',
  'revolution',
  'wellspring',
  'fount',
  'source',
  'fusion',
  'canopy',
  'flow',
  'network',
  'current',
  'transmission',
  'oasis',
  'quantum shift',
  'paradigm shift',
  'metamorphosis',
  'harmonizing',
  'reimagining',
  'rekindling',
  'unifying',
  'ozmosis',
  'vision',
  'uprising',
  'explosion',
  'transmutation'
];

var ing = [
  'flowering',
  'unfolding',
  'blossoming',
  'awakening',
  'deepening',
  'refining',
  'maturing',
  'evolving',
  'summoning',
  'unveiling',
  'redefining',
  'condensing',
  'ennobling',
];

var ingBad = [
   'troubling',
   'unsettling',
   'forbidding',
   'menacing',
   'alarming',
   'weakening',
   'brooding',
   'agonising',
   'threatening',
   'depressing',
   'stalking'
]

var adj = [
  'enlightened',
  'zero-point',
  'quantum',
  'high-frequency',
  'Vedic',
  'non-dual',
  'conscious',
  'sentient',
  'sacred',
  'infinite',
  'primordial',
  'ancient',
  'powerful',
  'spiritual',
  'higher',
  'advanced',
  'internal',
  'sublime',
  'technological',
  'dynamic',
  'life-affirming',
  'sensual',
  'unrestricted',
  'ever-present',
  'endless',
  'ethereal',
  'astral',
  'cosmic',
  'spatial',
  'transformative',
  'unified',
  'non-local',
  'mystical',
  'divine',
  'self-aware',
  'magical',
  'amazing',
  'interstellar',
  'unlimited',
  'authentic',
  'angelic',
  'karmic',
  'psychic',
  'pranic',
  'consciousness-expanding',
  'perennial',
  'heroic',
  'archetypal',
  'mythic',
  'intergalatic',
  'holistic',
  'joyous',
  'sublime', 
  'external',
  'sacred',
  'ayurvedic',
  'ephemeral',
  'outlandish'
];

var adjBig = [
  'epic',
  'unimaginable',
  'colossal',
  'unfathomable',
  'magnificent',
  'enormous',
  'jaw-dropping',
  'ecstatic',
  'powerful',
  'untold',
  'astonishing',
  'incredible',
  'breathtaking',
  'staggering',
  'humongous',
  'hidden',
  'unspoken'
];

var adjBad = [
  'evil',
  'stalking',
]

var adjWith = [
  'aglow with',
  'buzzing with',
  'beaming with',
  'full of',
  'overflowing with',
  'radiating',
  'bursting with',
  'electrified with',
  'gleaming with',
  'energized with',
  'constructed of',
];

var adjPrefix = [
  'ultra-',
  'supra-',
  'hyper-',
  'pseudo-',
  'nano-'
];

var vtMass = [
  'inspire',
  'integrate',
  'ignite',
  'discover',
  'rediscover',
  'foster',
  'release',
  'manifest',
  'harmonize',
  'engender',
  'bring forth',
  'bring about',
  'create',
  'spark',
  'reveal',
  'generate',
  'leverage'
];

var vtPerson = [
  'enlighten',
  'inspire',
  'empower',
  'unify',
  'strengthen',
  'recreate',
  'fulfill',
  'change',
  'develop',
  'heal',
  'awaken',
  'synergize',
  'ground',
  'bless',
  'beckon',
  'transform'
];

var viPerson = [
  'exist',
  'believe',
  'grow',
  'live',
  'dream',
  'reflect',
  'heal',
  'vibrate',
  'self-actualize',
  'seek'
];

var vtDestroy = [
  'destroy',
  'eliminate',
  'shatter',
  'disrupt',
  'sabotage',
  'exterminate',
  'obliterate',
  'eradicate',
  'extinguish',
  'erase',
  'confront',
  'diminish',
  'destabilize'
];

var nTheXOf = [
  'richness',
  'truth',
  'growth',
  'nature',
  'healing',
  'knowledge',
  'meaning',
  'purpose',
  'need'
];

var ppPerson = [
  'awakened',
  're-energized',
  'recreated',
  'reborn',
  'guided',
  'aligned'
];

var ppThingPrep = [
  'enveloped in',
  'transformed into',
  'nurtured by',
  'opened by',
  'immersed in',
  'engulfed in',
  'baptized in'
];

var fixedAdvP = [
  'through non-local interactions',
  'inherent in nature',
  'at the quantum level',
  'at the speed of light',
  'of unfathomable proportions',
  'on a cosmic scale',
  'devoid of self',
  'of the creative act',
];

var fixedAdvPPlace = [
  'in this dimension',
  'outside time',
  'within the Godhead',
  'at home in the cosmos',
];

var fixedNP = [
  'expanding wave functions',
  'superpositions of possibilities',
  'electromagnetic forces',
  'electromagnetic resonance',
  'molecular structures',
  'atomic ionization',
  'electrical impulses',
  'a resonance cascade',
  'bio-electricity',
  'ultrasonic energy',
  'sonar energy',
  'vibrations',
  'frequencies',
  'four-dimensional superstructures',
  'ultra-sentient particles',
  'sub-atomic particles',
  'chaos-driven reactions',
  'supercharged electrons',
  'supercharged waveforms',
  'pulses',
  'transmissions',
  'morphogenetic fields',
  'bio-feedback',
  'meridians',
  'morphic resonance',
  'cellular knowledge',
  'quantum information'
];

var nSubject = [
  'alternative medicine',
  'astrology',
  'tarot',
  'crystal healing',
  'the akashic record',
  'feng shui',
  'acupuncture',
  'homeopathy',
  'aromatherapy',
  'ayurvedic medicine',
  'faith healing',
  'prayer',
  'astral projection',
  'Kabala',
  'reiki',
  'naturopathy',
  'numerology',
  'affirmations',
  'the Law of Attraction'
];

var vOpenUp = [
  'open up',
  'give us access to',
  'enable us to access',
  'remove the barriers to',
  'clear a path toward',
  'let us access',
  'tap into',
  'align us with'
];

var vTraverse = [
  'traverse',
  'walk',
  'follow',
  'engage with',
  'go along',
  'roam',
  'navigate',
  'wander',
  'embark on',
  'lead'
];

var advAlways = [
  'always',
  'wholly',
  'consistently',
  'repeatedly',
  'everlastingly',
  'eternally',
  'endlessly',
  'perpetually',
  'forever'
];

var advPartly = [
   'partly', 
   'incompletely',
   'inadequately',  
];

var timesPlural = [
   'times',
   'days',
   'nights',
   'solar cycles',
   'eons',
   'moments',
   'years',
   'days of judgement'
];

var vBegin = [
   'begin',
   'start',
   'find',
   'actualize',
   'make',
   'initiate',
   'commence',
   'lead',
   'establish'
];

var vFeel = [
   'feel',
   'touch',
   'sense',
   'see',
   'realize',
   'believe',
   'listen'
];

var myFriend = [
    'my friend',
    'my sister',
    'my brother',
    'connected one',
    'awakened one',
    'fellow warrior',
    'kindred spirit',
    'spirit warrior'
];

var vGreeting = [
   'hey',
   'hello',
   'ciao',
   'aloha',
   'my brother',
   'my friend',
   'my sister',
];

var nConfirmation = [
   'yes',
   'surely',
   'sure',
   'of course',
   'definitely',
   'certainly',
];

var nMotor = [
   'driver',
   'primus motor',
   'incentive',
   'driving force',
   'manipulator',
   'animator'
];

var vCallingTo= [
   'reaching to',
   'calling to',
   'stretching to',
   'embracing',
   'encompassing',
   'spreading to',
   'spanning to'         
];

var vThink = [
   'think',
   'feel',
   'sense', 
   'understand',
   'acknowledge',
   'approve',
   'realize',
   'believe'
];

var nReason = [
   'goal',
   'reason',
   'ambition',
   'intent',
   'purpose',
   'objective',
   'destination',
   'desire',
   'target',
];

var nInstitution = [
   'science',
   'church',
   'politics',
   'meditation',
   'society'
];

var nSign = [
   'sign',
   'symbol',
   'omen',
   'premonition',
   'harbinger',
   'auspice',
   'augury'
];

var vCome = [
   'come',
   'manifest',
   'materialize',
   'transpire',
   'occur'
];

var nPersonLife = [
    'day',
    'life',
    'mind',
    'soul',
    'existence',
    'third eye',
    'heart',
    'thruth'
];

var nBattle = [
    'battle',
    'confrontation',
    'conflict',
    'struggle',
    'collision',
    'disharmony'
];

var adjPresent = [
    'prominent',
    'present',
    'evident',
    'current',
    'in process',
    'extant',
];

var nExploration = [
     'exploration',
     'research',
     'analysis',
     'expedition',
     'study',
     'inspection',
     'introspection',
     'examination'
];

var adjCareful = [
     'careful',
     'meticulous',
     'rigorous',
     'vigilant',
     'cautious',
     'mindful',
     'conscious',
     'sensible',
     'enlightened'
];

var vFound = [
     'found',
     'started',
     'begun',
     'created',
     'formed',
     'initiated',
     'realized',
     'planted'
];

var sentencePatterns = new Array();

//explaining
sentencePatterns[0] = [
'<> nMass is the <> nMotor of <> nMass',
'<> nMass is the nTheXOf of <> nMass, and of us',
'You and I are <> nPersonPlural of the <> nCosmos',
'We viPerson as <> fixedNP',
'We viPerson, we viPerson, we are reborn in <> nCosmos',
'Nothing is impossible for <> nPerson',
'This <> life is nothing short of a <> ing nOf of adj <> nMass',
'<> consciousness consists of fixedNP of <> quantum nEnergy',
'nMass means a <> ing of the <> adj',
'The <> nReason of fixedNP is to plant the <> seeds of <> nMass rather than <> nMassBad',
'<> nMass is a <> constant',
'By <> ing, we viPerson as <> beings',
'This <> nCosmos is adjWith fixedNP',
'To vTraverse the <> nPath is to become one with it'
];

//warnings
sentencePatterns[1] = [
'We can no longer afford to live with <> nMassBad',
'Without <> nMass, one cannot viPerson',
'Only a nPerson of the <> nCosmos may vtMass this <> nOf of <> nMass',
'vGreeting, <> nPerson, you must take a stand against <> nMassBad',
'nConfirmation, it is possible to vtDestroy the <> things that can vtDestroy us, but not without <> nMass on our side',
'<> nMassBad is the <> antithesis of <> nMass',
'vGreeting, you may be ruled by <> nMassBad without realizing it. Do not let it vtDestroy the nTheXOf of your <> nPath',
'the <> complexity of the present <> time seems to demand a ing of our <> nOurPlural if we are going to survive',
'<> nMassBad is born in the <> gap where <> nMass has been excluded',
'Where there is <> nMassBad, <> nMass cannot thrive',
'In these ingBad <> timesPlural the <> nMassBad can vtDestroy all adj <> nMass'
];

//future hope
sentencePatterns[2] = [
'Soon there will be a ing of <> nMass the likes of which the <> nCosmos has never seen',
'It is time to take <> nMass to the next <> level',
'Imagine a <> ing of what could be',
'<> Eons from now, we <> nPersonPlural will viPerson like never before as we are ppPerson by the <> nCosmos',
'This is a <> nSign of <> timesPlural to vCome',
'The <> future will be a adj <> ing of <> nMass',
'This <> nPath never ends',
'We must learn how to lead adj <> lives in the face of <> nMassBad',
'We must vtPerson our <> selves and vtPerson others',
'The nOf of <> nMass is now happening worldwide',
'We are being called to explore the <> nCosmos itself as a <> interface between <> nMass and <> nMass',
'It is in <> ing that we are ppPerson',
'This <> nCosmos is approaching a <> tipping point'
];

//you and your problems
sentencePatterns[3] = [
'Although you, myFriend, may not vThink it, you are <> adj',
'<> nPerson, look within and vtPerson yourself',
'vGreeting, <> nPerson, have you vFound your <> nPath?',
'How should you vTraverse this <> adj <> nCosmos?',
'It can be difficult to know where to vBegin your <> nPath',
'If you have never experienced this <> nOf fixedAdvP, it can be difficult to viPerson',
'This <> nCosmos is vCallingTo you via fixedNP. Can you vFeel it?',
'vGreeting, adj <> nPerson, are you able to vFeel the <> nCosmos? Do you really vFeel it?',
'vGreeting, myFriend. Do you vThink that our <> nOurPlural are ppThingPrep adj <> nMassBad?',
'myFriend, how does ing <> one vFeel this, adj <> nMass?',
'vGreeting, <> nPerson, is your nPersonLife full of adj <> nEnergy?'
];

//history
sentencePatterns[4] = [
'Throughout <> history, <> humans have been interacting with the <> nCosmos via fixedNP',
'<> nCosmos has advAlways been adjWith <> nPersonPlural whose <> nOurPlural are ppThingPrep <> nMass',
'Our adj <> conversations with other <> nPersonPlural have led to a ing of adjPrefix adj <> consciousness',
'vGreeting, we are in the midst of a adj <> ing of <> nMass that will vOpenUp the <> nCosmos itself',
'Who are we, <> nPersonPlural? Where on the great <> nPath will we be ppPerson?',
'vGreeting, we are at a <> crossroads of <> nMass and <> nMassBad',
'Today, nInstitution tells us that the <> essence of <> nature is <> nMass',
'This adj <> nMass requires adjCareful <> nExploration'
// 'Even nProphet '
];

//selling point
sentencePatterns[5] = [
'Through <> nSubject, our <> nOurPlural are ppThingPrep nMass',
'nSubject may be the <> solution to what\'s holding you back from a adjBig nOf of <> nMass',
'myFriend, you will soon be ppPerson by a <> nEnergy deep within yourself -- a <> nEnergy that is adj, adj',
'As you viPerson, you will enter into infinite <> nMass that transcends <> understanding',
'The <> nBattle between adj <> nMass and ingBad <> nMassBad is advAlways adjPresent',
'The nReason of <> nInstitution is to advAlways vBegin <> nOf of <> nMass',
'Are you with us, myFriend, the adj <> nPerson?',
'For every ppPerson <> nPerson there comes a <> time when one needs to viPerson oneself',
'Do you see this adj <> nMass within your grasp adj nPerson?'
];

// deepCopy function taken from:
// http://james.padolsey.com/javascript/deep-copying-of-objects-and-arrays/
function deepCopy(obj) {
    if (Object.prototype.toString.call(obj) === '[object Array]') {
        var out = [], i = 0, len = obj.length;
        for ( ; i < len; i++ ) {
            out[i] = arguments.callee(obj[i]);
        }
        return out;
    }
    if (typeof obj === 'object') {
        var out = {}, i;
        for ( i in obj ) {
            out[i] = arguments.callee(obj[i]);
        }
        return out;
    }
    return obj;
}

function removeSentence(topic, element) {

  if (element > -1) {
    sentencePatternsClone[topic].splice(element, 1);
  }

}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function randomInt(max) {
    return Math.floor(Math.random()*(max+1));
}


function retrieveRandomWordOfType(type) {
  var max = type.length - 1;
  var rand = randomInt(max);
  var result = type[rand];
  return result;
}

function generateSentence(topic) {

  var length = sentencePatternsClone[topic].length;

  // generate random sentence pattern
  var patternNumber = randomInt(length - 1);
  var pattern = sentencePatternsClone[topic][patternNumber];

  if (typeof pattern == 'undefined') {
    console.log('ran out.');
    return ":( ";
  }

  var pattern = pattern.replace(/([\.,;\?])/g,' $1');
  var pattern = pattern.split(' ');

  // remove the pattern from the sentence array so it isn't re-used
  removeSentence(topic, patternNumber);

  // console.log('sentencePatternsClone.length is now ' + sentencePatternsClone.length);
  if (sentencePatternsClone[topic].length == 0) {
    sentencePatternsClone.splice(topic, 1);
    // console.log('topic removed!');
    // console.log('sentencePatternsClone.length is now ' + sentencePatternsClone.length);
  }

  var result = "";

  for (var x in pattern) {

    switch (pattern[x]) {
      case 'nCosmos': result += retrieveRandomWordOfType(nCosmos);
      break;
      case 'nPerson': result += retrieveRandomWordOfType(nPerson);
      break;
      case 'nPersonPlural': result += retrieveRandomWordOfType(nPersonPlural);
      break;
      case 'nMass': result += retrieveRandomWordOfType(nMass);
      break;
      case 'nMassBad': result += retrieveRandomWordOfType(nMassBad);
      break;
      case 'nPath': result += retrieveRandomWordOfType(nPath);
      break;
      case 'nOurPlural': result += retrieveRandomWordOfType(nOurPlural);
      break;
      case 'nOf': result += retrieveRandomWordOfType(nOf);
      break;
      case 'ing': result += retrieveRandomWordOfType(ing);
      break;
      case 'adj': result += retrieveRandomWordOfType(adj);
      break;
      case 'adjBig': result += retrieveRandomWordOfType(adjBig);
      break;
      case 'adjWith': result += retrieveRandomWordOfType(adjWith);
      break;
      case 'adjPrefix': result += retrieveRandomWordOfType(adjPrefix);
      break;
      case 'vtMass': result += retrieveRandomWordOfType(vtMass);
      break;
      case 'vtPerson': result += retrieveRandomWordOfType(vtPerson);
      break;
      case 'vtDestroy': result += retrieveRandomWordOfType(vtDestroy);
      break;
      case 'viPerson': result += retrieveRandomWordOfType(viPerson);
      break;
      case 'nTheXOf': result += retrieveRandomWordOfType(nTheXOf);
      break;
      case 'ppPerson': result += retrieveRandomWordOfType(ppPerson);
      break;
      case 'ppThingPrep': result += retrieveRandomWordOfType(ppThingPrep);
      break;
      case 'fixedAdvP': result += retrieveRandomWordOfType(fixedAdvP);
      break;
      case 'fixedAdvPPlace': result += retrieveRandomWordOfType(fixedAdvPPlace);
      break;
      case 'fixedNP': result += retrieveRandomWordOfType(fixedNP);
      break;      
      case 'nSubject': result += retrieveRandomWordOfType(nSubject);
      break;
      case 'vOpenUp': result += retrieveRandomWordOfType(vOpenUp);
      break;      
      case 'vTraverse': result += retrieveRandomWordOfType(vTraverse);
      break;
      case 'nEnergy': result += retrieveRandomWordOfType(nEnergy);
      break;
      case 'advAlways': result += retrieveRandomWordOfType(advAlways);
      break;
      case 'advPartly': result += retrieveRandomWordOfType(advPartly);
      break;
      case 'ingBad': result += retrieveRandomWordOfType(ingBad);
      break;
      case 'timesPlural': result += retrieveRandomWordOfType(timesPlural);
      break;
      case 'vBegin': result += retrieveRandomWordOfType(vBegin);
      break;
      case 'vFeel': result += retrieveRandomWordOfType(vFeel);
      break;
      case 'vGreeting': result += retrieveRandomWordOfType(vGreeting);
      break;
      case 'myFriend': result += retrieveRandomWordOfType(myFriend);
      break;
      case 'nConfirmation': result += retrieveRandomWordOfType(nConfirmation);
      break;
      case 'nMotor': result += retrieveRandomWordOfType(nMotor);
      break;
      case 'vCallingTo': result += retrieveRandomWordOfType(vCallingTo);
      break;
      case 'vThink': result += retrieveRandomWordOfType(vThink);
      break;
      case 'nReason': result += retrieveRandomWordOfType(nReason);
      break;
      case 'nInstitution': result += retrieveRandomWordOfType(nInstitution);
      break;
      case 'nSign': result += retrieveRandomWordOfType(nSign);
      break;
      case 'vCome': result += retrieveRandomWordOfType(vCome);
      break;
      case 'nPersonLife': result += retrieveRandomWordOfType(nPersonLife);
      break;
      case 'nBattle': result += retrieveRandomWordOfType(nBattle);
      break;
      case 'adjPresent': result += retrieveRandomWordOfType(adjPresent);
      break;
      case 'nExploration': result += retrieveRandomWordOfType(nExploration);
      break;
      case 'adjCareful': result += retrieveRandomWordOfType(adjCareful);
      break;
      case 'vFound': result += retrieveRandomWordOfType(vFound);
      break;
      default: result += pattern[x];
    }

    result += ' ';
  }

  result = result.trim();
  result = capitalizeFirstLetter(result);

  if (result.charAt(result.length-1) != '?') {
    result += '. ';
  } else {
    result += ' ';
  }

  // remove spaces before commas/periods/semicolons
  result = result.replace(/ ([,\.;\?])/g,'$1');

  return result;
}

function generateText(numberOfSentences, sentenceTopic) {

  var fullText = "";

  for (var i = 0; i < numberOfSentences; i++) {

    fullText += generateSentence(sentenceTopic);

    // in case the topic got deleted
    if (typeof sentencePatternsClone[sentenceTopic] == 'undefined') {
      sentenceTopic = randomInt(sentencePatternsClone.length - 1);
      // console.log('topic reset to ' + sentenceTopic);
    }

  } 

  // replace 'a [vowel]' with 'an [vowel]'
  // I added a \W before the [Aa] because one time I got
  // "Dogman is the antithesis of knowledge" :)
  fullText = fullText.replace(/(^|\W)([Aa]) ([aeiou])/g,'$1$2n $3');

  // take care of prefixes (delete the space after the hyphen)
  fullText = fullText.replace(/- /g,'-');

  return fullText;

}

var args = process.argv.slice(2);
sentencePatternsClone = deepCopy(sentencePatterns);
sentenceTopic = randomInt(sentencePatternsClone.length - 1);
//console.log(generateText(args[0], sentenceTopic));
console.log(generateText(args[0], sentenceTopic));




