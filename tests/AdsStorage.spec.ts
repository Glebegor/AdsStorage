import { Blockchain, SandboxContract, TreasuryContract } from '@ton/sandbox';
import { toNano } from '@ton/core';
import { AdsStorage } from '../wrappers/AdsStorage';
import '@ton/test-utils';

describe('AdsStorage', () => {
    let blockchain: Blockchain;
    let deployer: SandboxContract<TreasuryContract>;
    let adsStorage: SandboxContract<AdsStorage>;

    beforeEach(async () => {
        blockchain = await Blockchain.create();

        adsStorage = blockchain.openContract(await AdsStorage.fromInit());

        deployer = await blockchain.treasury('deployer');

        const deployResult = await adsStorage.send(
            deployer.getSender(),
            {
                value: toNano('0.05'),
            },
            {
                $$type: 'Deploy',
                queryId: 0n,
            }
        );

        expect(deployResult.transactions).toHaveTransaction({
            from: deployer.address,
            to: adsStorage.address,
            deploy: true,
            success: true,
        });
    });

    it('should deploy', async () => {
        // the check is done inside beforeEach
        // blockchain and adsStorage are ready to use
    });
});
