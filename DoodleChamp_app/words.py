from DoodleChamp_app.models import Words

words= "alligator, america, angle, ant, applause, apple, arch, arm, army, artist, avocado, baby, backbone, bag, baker, ball, band, baseball, basin, basket, bath, bathroom, battery, bed, bedbug, bee, beehive, bell, berry, bicycle, bird, birthday cake, birthday, blade, bleach, board, boat, bomb, bone, bonnet, book, boot, bottle, bow tie, box, boy, brain, brake, branch, brick, bridge, bruise, brush, bucket, bulb, button, cabin, cake, camera, card, cardboard, carriage, cart, cat, ceiling, chain, chalk, chameleon, charger, cheerleader, cheese, chef, chess, chime, chin, church, circle, circus, cliff, cloak, clock, cloud, coach, coal, coat, collar, comb, comedian, computer, convertible, cord, cow, cowboy, cruise, crust, cup, cupcake, curtain, cushion, darts, deep, dent, dentist, diving, dog, doghouse, door, doormat, drain, drawer, dream, dress, drip, drop, dust, ear, egg, electricity, engine, extension cord, eye, face, farm, feather, finger, firefighter, fireman, fish, fizz, flag, flagpole, floor, flute, fly, fog, foot, fork, fowl, frame, french fries, frog, garbage, garden, garfield, gate, giant, girl, glove, goat, goblin, golden retriever, gun, hair dryer, hair, hammer, hand, handle, hat, head, headphones, heart, hockey, hook, hopscotch, horn, horse, hospital, hot dog, hot tub, house, houseboat, hurdle, internet, island, jewel, joke, kettle, key, knee, kneel, knife, knight, knot, koala, lace, lap, lawnmower, leaf, leak, leg, light bulb, lighthouse, line, lip, lock, mailman, map, mascot, match, mattress, money, monkey, moon, mouth, muscle, mushroom, music, nail, nature, neck, needle, neet, nerve, net, newspaper, nightmare, nose, nut, oar, office, orange, outside, oven, owl, pajamas, parcel, park, password, peach, pen, pencil, pharmacist, photograph, picnic, picture, pig, pilot, pin, pineapple, ping pong, pinwheel, pipe, pirate, plane, plank, plate, plough, pocket, pool, popsicle, post office, pot, potato, prison, pump, puppet, purse, queen, quilt, raft, rail, raincoat, rat, ray, receipt, ring, rod, roof, root, rug, safe, sail, salmon, salt and pepper, sandbox, scale, school, scissors, screw, season, seed, shallow, shampoo, sheep, sheets, shelf, ship, shirt, shoe, shrink, skate, ski, skin, skirt, sleep, snake, sneeze, snowball, sock, song, spade, speakers, sponge, spoon, spring, sprinkler, square, stamp, star, state, station, stem, stick, stingray, stocking, stomach, store, street, suitcase, sun, sunburn, sushi, swamp, sweater, table, tail, teapot, thief, think, thread, throat, thumb, ticket, time machine, tiptoe, toe, tongue, tooth, town, train, tray, treasure, tree, trip, trousers, turtle, tusk, tv, umbrella, violin, wall, watch, watering can, wax, wedding dress, wheel, whip, whistle, wig, window, wing, wire, worm, yardstick, zoo"
word_list = words.split(sep=", ")
word_dict = {}
for i in word_list:
    length = len(i)
    if length <= 4:
        word_dict[i] = 50
    elif length <= 7:
        word_dict[i] = 100
    elif length <= 11:
        word_dict[i] = 150
    elif length > 11:
        word_dict[i] = 200

word_ = {}

for i in word_list:
            Words.objects.create(word = i, point_value = word_dict[i])

if __name__ == '__main__':

    print(word_dict)