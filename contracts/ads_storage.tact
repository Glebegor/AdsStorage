import "@stdlib/deploy";

struct Bid {
    amount: Int as uint128;
    hash: Bytes;
    link: String;
}

contract AdsStorage with Deployable {
    const FEE: Int = ton("0.1");

    bids: map<Address, Bid>;
    startTime: Int as uint64;
    endTime: Int as uint64;
    maxBid: Bid;
    maxBidder: Address;
    
    init(startTime: Int, endTime: Int) {
        self.startTime = startTime;
        self.endTime = endTime;
    }

    receive("placeBid") {
        let amount: Int = context.sendRawMsg.data.parse(Int);
        let hash: Bytes = context.sendRawMsg.data.parse(Bytes);
        let link: String = context.sendRawMsg.data.parse(String);

        require(now() >= self.startTime && now() < self.endTime, "Auction is not active");

        let currentBid: Bid? = self.bids.get(sender());
        let currentBidAmount: Int = currentBid ? currentBid.amount : 0; // Если currentBid == null, то currentBidAmount = 0
        
        if (amount > currentBidAmount) {
            let ctx:Context = context();
            let newAddress: Address = get.sender(); // Сохраняем адрес отправителя в переменную
            let newBid: Bid = Bid{amount: amount, hash: hash, link: link}; // Создаем новый экземпляр структуры Bid
            currentBid.set(ctx.sender , ctx.newBid); // Присваиваем значение в словарь по ключу newAddress

            if (amount > self.maxBid.amount) {
                self.maxBid = Bid{amount: amount, hash: hash, link: link};
                self.maxBidder = sender();
            }
        }
    }

    receive("endAuction") {
        require(now() >= self.endTime, "Auction is still active");

        // Отправка ссылки победителя на бэкенд ??
        // Получение ставки победителя
        let winnerAddr:Address = self.maxBid.addr;
        let winnerBid:Bid = self.maxBid.bid;
        // Отправка ссылки победителя на бэкенд
        send(SendParameters{
            to: backendAddress, // адрес бэкенда
            value: bid - self.FEE, // не отправляем токены
            mode: SendRemainingValue | SendIgnoreErrors, // отправить все полученные токены и игнорировать ошибки
            body: msg.value("receiveWinnerLink", maxBid.link) // тело сообщения с ссылкой победителя
        });

            // Возврат средств проигравшим участникам
        for ((addr, bid) : self.bids.entries()) {
            if (addr != winnerAddr) {
                addr.transfer(bid.amount - self.FEE, true);
            }
        }
    }
        

    

    get fun auctionData(): (Int, Int, Bid, Address) {
        return (self.startTime, self.endTime, self.maxBid, self.maxBidder );
    }
    
}

