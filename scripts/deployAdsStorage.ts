import { toNano } from '@ton/core';
import { AdsStorage } from '../wrappers/AdsStorage';
import { NetworkProvider } from '@ton/blueprint';

export async function run(provider: NetworkProvider) {
    const adsStorage = provider.open(await AdsStorage.fromInit());

    await adsStorage.send(
        provider.sender(),
        {
            value: toNano('0.05'),
        },
        {
            $$type: 'Deploy',
            queryId: 0n,
        }
    );

    await provider.waitForDeploy(adsStorage.address);

    // run methods on `adsStorage`
}
