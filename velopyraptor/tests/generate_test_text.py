f = open('latin_text', 'w')
for i in xrange(5000):
    text = "Lorem ipsum dolor sit amet, est malis molestiae no,\nrebum" \
           "mediocrem vituperatoribus qui et. Quando intellegam ne mea," \
           " utroque\n voluptua sensibus nam te. In duo accusam accusamus," \
           " mea ad iriure detracto\nsigniferumque. Veri complectitur" \
           " concludaturque te sed. Ad pri intellegam\ncomprehensam. " \
           "Detracto pertinax pri ex, usu ne animal mandamus, sit ut\n" \
           "delectus forensibus.\n\n"
    f.write(text)
f.close()
