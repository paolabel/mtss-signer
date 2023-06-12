from mtsssigner.signer import sign
from mtsssigner.signature_scheme import SigScheme

DIGEST_SIZE = 256
DIGEST_SIZE_BYTES = 32
N_BLOCKS = 9
KEY_MODULUS = 2048

correct_sigma = ("c91dc78bba3aa8b97123f362e714953179d48d80b51472ffcaa585df06cbec69"
                 "12ca991cfbd66cb06fbdea2c3ade38e21c0a093c2eaa0471c3c04a6d290db41b"
                 "3e60d3850b35912815d81fe99f3d8e71bd58263e1491a81307f1118eae9166de"
                 "910d356ac29e0732d284ea4d13a58666951de0f92b25b9312d47ceb968b4d428"
                 "445c2fe46cb98961175ae2cc5b8847a1817e4941058d30e11d70419e13dbd3bf"
                 "b2c2f2f1f06c6cbc9fc90d0f2656749a4f0ef81c6538064f9feac4a4054e2994"
                 "88567f2b495768ba1e5db1365abc120639629aabf4b396fa30bf9f17fb2c16d1"
                 "2d1b676bdd6b5d1386e66543d4e2859587d86a493f32828de05a7c66ba330d03"
                 "6693ce98fc267da46e3f1250ca4caafb9bcb9a61cbdf91dab6a6501870759674"
                 "0e2ca93b265e28dd964c8ac71b1a393b7480c8e60e5fa92c282176f205fe4fb6"
                 "89bfdbe9cbd0748c0868664fb6ca7cab8594dd0ad525bb29b2c827c5ff7b878eae97f02e00870d6e27b60890751aa9be07e2f3100db02d99f1b48b6f4460e2445d323f36474a8d9e857204b4a1d97a9c0f959a31dc56035d8bd8a48016332c7e72608aaf8de261b44fd8c44134ee6513fdb4f9273bae52015660406eec77df4ffb4bf99dc31ec1b28cc88d5342b94a6c6d699d6f35b2968a613dd3357372df5ea8e124a89e9825d88bce4d0bebeb416796007c7c41b6ddb88063b3cd6835cb16f08d6b6cd93405766c6ff024990181aabf37713e5c854b0696474d036da85f0321ecedf6fab3d9cb9c96fb3e5358a8bbf15d5a7ac1a6e41bf5bcba11d468121d")

correct_signature = "89bfdbe9cbd0748c0868664fb6ca7cab8594dd0ad525bb29b2c827c5ff7b878eae97f02e00870d6e27b60890751aa9be07e2f3100db02d99f1b48b6f4460e2445d323f36474a8d9e857204b4a1d97a9c0f959a31dc56035d8bd8a48016332c7e72608aaf8de261b44fd8c44134ee6513fdb4f9273bae52015660406eec77df4ffb4bf99dc31ec1b28cc88d5342b94a6c6d699d6f35b2968a613dd3357372df5ea8e124a89e9825d88bce4d0bebeb416796007c7c41b6ddb88063b3cd6835cb16f08d6b6cd93405766c6ff024990181aabf37713e5c854b0696474d036da85f0321ecedf6fab3d9cb9c96fb3e5358a8bbf15d5a7ac1a6e41bf5bcba11d468121d"

correct_message_hash = "0e2ca93b265e28dd964c8ac71b1a393b7480c8e60e5fa92c282176f205fe4fb6"

correct_t = ["c91dc78bba3aa8b97123f362e714953179d48d80b51472ffcaa585df06cbec69", 
             "12ca991cfbd66cb06fbdea2c3ade38e21c0a093c2eaa0471c3c04a6d290db41b", 
             "3e60d3850b35912815d81fe99f3d8e71bd58263e1491a81307f1118eae9166de", 
             "910d356ac29e0732d284ea4d13a58666951de0f92b25b9312d47ceb968b4d428", 
             "445c2fe46cb98961175ae2cc5b8847a1817e4941058d30e11d70419e13dbd3bf", 
             "b2c2f2f1f06c6cbc9fc90d0f2656749a4f0ef81c6538064f9feac4a4054e2994", 
             "88567f2b495768ba1e5db1365abc120639629aabf4b396fa30bf9f17fb2c16d1", 
             "2d1b676bdd6b5d1386e66543d4e2859587d86a493f32828de05a7c66ba330d03", 
             "6693ce98fc267da46e3f1250ca4caafb9bcb9a61cbdf91dab6a6501870759674"]

correct_t_plus_messagehash_hash = "1d41b59281f17b1e17fde728fd72f22315cd31d19f67d1ea68cb88a5eeefdd73"

def test_sign_rsa2048_sha256():
    sig_scheme = SigScheme("PKCS#1 v1.5", "SHA256")
    signature = sign(sig_scheme, "msg/sample_message.txt", "keys/private_openssl1-1.pem", k=2)

    t = signature[:-int(KEY_MODULUS/8)]
    t_signature = signature[-int(KEY_MODULUS/8):]
    signature_message_hash = t[-int(DIGEST_SIZE_BYTES):]
    joined_hashed_tests: bytearray = signature[:-int(DIGEST_SIZE_BYTES)]
    hashed_tests = [
        joined_hashed_tests[i:i+int(DIGEST_SIZE_BYTES)]
        for i in range(0, len(joined_hashed_tests), int(DIGEST_SIZE_BYTES))]

    for t in range(len(correct_t)):
        assert(hashed_tests[t].hex() == correct_t[t])
    assert(signature_message_hash.hex() == correct_message_hash)
    assert(t_signature.hex() == correct_signature)
    assert(signature.hex() == correct_sigma)
