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
  'soul'
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
  'bondage',
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
  'external'
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
  'staggering'
];

var adjWith = [
  'aglow with',
  'buzzing with',
  'beaming with',
  'full of',
  'overflowing with',
  'radiating',
  'bursting with',
  'electrified with'
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
  'morphic resonance'
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
  'embark on'
];

var sentencePatterns = new Array();

//explaining
sentencePatterns[0] = [
'nMass is the driver of nMass',
'nMass is the nTheXOf of nMass, and of us',
'You and I are nPersonPlural of the nCosmos',
'We exist as fixedNP',
'We viPerson, we viPerson, we are reborn',
'Nothing is impossible',
'This life is nothing short of a ing nOf of adj nMass',
'Consciousness consists of fixedNP of quantum energy. "Quantum" means a ing of the adj',
'The goal of fixedNP is to plant the seeds of nMass rather than nMassBad',
'nMass is a constant',
'By ing, we viPerson',
'The nCosmos is adjWith fixedNP',
'To vTraverse the nPath is to become one with it',
'Today, science tells us that the essence of nature is nMass',
'nMass requires exploration'
];

//warnings
sentencePatterns[1] = [
'We can no longer afford to live with nMassBad',
'Without nMass, one cannot viPerson',
'Only a nPerson of the nCosmos may vtMass this nOf of nMass',
'You must take a stand against nMassBad',
'Yes, it is possible to vtDestroy the things that can vtDestroy us, but not without nMass on our side',
'nMassBad is the antithesis of nMass',
'You may be ruled by nMassBad without realizing it. Do not let it vtDestroy the nTheXOf of your nPath',
'the complexity of the present time seems to demand a ing of our nOurPlural if we are going to survive',
'nMassBad is born in the gap where nMass has been excluded',
'Where there is nMassBad, nMass cannot thrive'
];

//future hope
sentencePatterns[2] = [
'Soon there will be a ing of nMass the likes of which the nCosmos has never seen',
'It is time to take nMass to the next level',
'Imagine a ing of what could be',
'Eons from now, we nPersonPlural will viPerson like never before as we are ppPerson by the nCosmos',
'It is a sign of things to come',
'The future will be a adj ing of nMass',
'This nPath never ends',
'We must learn how to lead adj lives in the face of nMassBad',
'We must vtPerson ourselves and vtPerson others',
'The nOf of nMass is now happening worldwide',
'We are being called to explore the nCosmos itself as an interface between nMass and nMass',
'It is in ing that we are ppPerson',
'The nCosmos is approaching a tipping point'
];

//you and your problems
sentencePatterns[3] = [
'Although you may not realize it, you are adj',
'nPerson, look within and vtPerson yourself',
'Have you found your nPath?',
'How should you navigate this adj nCosmos?',
'It can be difficult to know where to begin',
'If you have never experienced this nOf fixedAdvP, it can be difficult to viPerson',
'The nCosmos is calling to you via fixedNP. Can you hear it?'
];

//history
sentencePatterns[4] = [
'Throughout history, humans have been interacting with the nCosmos via fixedNP',
'Reality has always been adjWith nPersonPlural whose nOurPlural are ppThingPrep nMass',
'Our conversations with other nPersonPlural have led to a ing of adjPrefix adj consciousness',
'Humankind has nothing to lose',
'We are in the midst of a adj ing of nMass that will vOpenUp the nCosmos itself',
'Who are we? Where on the great nPath will we be ppPerson?',
'We are at a crossroads of nMass and nMassBad'
// 'Even nProphet '
];

//selling point
sentencePatterns[5] = [
'Through nSubject, our nOurPlural are ppThingPrep nMass',
'nSubject may be the solution to what\'s holding you back from a adjBig nOf of nMass',
'You will soon be ppPerson by a power deep within yourself -- a power that is adj, adj',
'As you viPerson, you will enter into infinite nMass that transcends understanding'
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

  // find how long the array of words is for given type
  var max = type.length - 1;

  // get a random number to represent a word in the array
  var rand = randomInt(max);

  var result = type[rand];

  // type.splice(rand,1); 
  // console.log(type);

  return result;

}

function generateSentence(topic) {

  var length = sentencePatternsClone[topic].length;

  // generate random sentence pattern
  var patternNumber = randomInt(length - 1);

  // console.log('sentencePatternsClone[' + topic + '].length = ' + (patternNumber+1));

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
console.log(generateText(args[0], sentenceTopic));





