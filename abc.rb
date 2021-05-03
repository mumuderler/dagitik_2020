MAGIC = 'ADFGVX'

def all_letters(str)
    str[/[a-zA-Z]+/]
end

def encode(message, alphabet, keyword)
    key = []
    
    key = keyword.split(//).uniq
    k1 = ""
    n = key.length

    for i in 0..n-1 do
        k1.concat(key.index(key[i]).to_s)
    end
    k = k1.split(//)
#   k = key.sort

    s = []
    s2 = []
    message.downcase.each_char { |c|
        if all_letters(c) then
            row = alphabet.index(c) / 6
            col = alphabet.index(c) % 6
            s += [MAGIC[row],MAGIC[col]]
        end
    }

    for i in k do
        i.step s.size,n do |j|
            s.join('')
        end
    end
    puts s
end

alfabe = "abcçdefgğhıijklmnoöprsştuüvyz......."
encode("I am going",alfabe,"cipher")
